import json, re
import numpy as np
from Read_and_write import read_and_write_data
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn import linear_model

stemmer = PorterStemmer()
rwd = read_and_write_data.Read_Data()
stop_words = set(stopwords.words('english'))

class Preprocessing:

  # Underscores multiword topics and optionally removes words
  # in size-n window around topics to increase conditional independence
  # of topics and the text.  Default window size is 0

  def process_topics(self, infile, topicfile, window_size=0):
    outfile = infile.replace("selected_", "bigram_")

    topics = rwd.read_topics(topicfile)
    topic_list = []
    for topic in topics:
      for a in topic:
        topic_list.append(a)
    topics = topic_list

    with open(infile) as file, open(outfile, 'w') as newfile:
      for line in file:
        data = json.loads(line)
        review = data["text"]
        review = review.lower()
        review = review.replace("'", "")
        review = re.sub("[^a-z]+", " ", review)

        for word in topics:
          ##searching bigrams in review text
          if " "+word+" " in review:
            if " " in word:
              oldword = word
              word = word.replace(" ", "_")
              review = review.replace(" "+oldword+" ", " "+word+" ")
              review = word_tokenize(review)
              ind = review.index(word)
              review[ind] = word
              review = " ".join(review[:ind-window_size]+[word]+review[(ind+1)+window_size:])

        # data["text"] = review
        data["text"] = " ".join([stemmer.stem(i) for i in review.split() if i not in stop_words])
        json.dump({'business_id':data['business_id'],  'user_id': data['user_id'], 'stars':data['stars'], 'text':data['text']}, newfile, ensure_ascii=True)
        newfile.write('\n')

    return outfile

  '''
  Builds the dictionary that maps features in the bag of words feature vectors to the words they represent
  Verbose is set to True as a default, which prints the number of reviews processed on every hundreth one.
  '''
  def write_dictionary(self, infile, outfile, verbose=True):
    f = open(infile, 'r')
    words = []
    i = 0
    for line in f:
      line = json.loads(json.loads(line))['text']
      text = word_tokenize(line)
      words = words + list(set(text))

      if verbose and i%100 == 0:
        print i
      i += 1

    f.close()

    word_counts = Counter(words)
    words = [k for k, v in word_counts.items() if v >= 50]

    f = open(outfile, 'w')
    for word in words:
      f.write(word.encode('utf-8') + "\n")

    f.close()

  '''
  Reviews are partitioned into 2 groups, 1 and 0(y-label)
      1 - if star rating>=4
      0 - if otherwise
  Each review text is converted to a feature vector of the size of words in the dictionary
  For each word in dictionary:
      1 - if word appears in the review
      0 - if otherwise
  Format: [label, feature_vector]
      all elements are separated by " "
  Verbose is set to True as a default, which prints the number of reviews processed on every hundreth one.
  '''
  def write_features(self, infile, dictfile, binary=True, cutoff=4, verbose=True):
    outfile = infile.replace("_review.json", "_features.txt")

    f = open(dictfile, 'r')
    words = []
    for line in f:
      words.append(line.strip())
    f.close()

    f = open(infile, 'r')
    reviews = []
    for line in f:
      reviews.append(line)
    f.close()

    f = open(outfile, 'w')
    i = 0
    for review in reviews:
      review = json.loads(json.loads(review))

      if binary:
        if review['stars'] >= cutoff:
          f.write("1")
        else:
          f.write("0")
        f.write(" ")
      else:
        f.write(str(review['stars']) + " ")

      review = review['text'].encode('utf-8')
      review = review.split()
      for word in words:
        if word in review:
          f.write("1")
        else:
          f.write("0")
        f.write(" ")
      f.write("\n")

      if verbose and i%100 == 0:
        print i
      i += 1

    f.close()

    return outfile

class Read_Data:

  def read_topics(self, infile):
    topics = []
    topic = []
    f = open(infile, 'r')
    for line in f:
      line = line.strip()
      if line != "":
        topic.append(line)
      else:
        topics.append(topic)
        topic = []
    topics.append(topic)
    return topics

  '''
  read dictionary into memory
  '''
  def read_dictionary(self, filename):
    f = open(filename, 'r')
    dictionary = []
    for line in f:
      line = line.replace("\n", "")
      dictionary.append(line)
    return dictionary

  '''
  read feature vectors from 'filename' into memory
  verbose set to True prints the totalnumber of reviews
  read in and the number of positive and negative reviews
  Verbose only supports 2 classes at this point
  '''
  def read_features(self, filename, verbose=False):
    f = open(filename, 'r')
    features = []
    labels = []
    i = 0

    if verbose:
      countpos = 0
      countneg = 0

    for line in f:
      line = line.split()
      try:
        labels.append(int(line[0]))
      except:
        print line[0]

      if verbose:
        if int(line[0]) == 1:
          countpos += 1
        elif int(line[0]) == 0:
          countneg += 1

      feats = []
      for j in range(1, len(line)):
        if "topic" in filename:
          feats.append(float(line[j]))
        else:
          feats.append(int(line[j]))
      features.append(feats)

    if verbose:
      print filename
      print str(len(features)) + " total reviews"
      print str(countpos) + " positive reviews"
      print str(countneg) + " negative reviews"

    return [features, labels]


class Topics:

  def write_model(self, log, topic, dictionary):
    coefs = list(log.coef_[0])

    f = open("topic_Models/"+topic[0]+'_model.txt', 'w')
    f.write("Weights for topic "+topic[0]+"\n\n")

    topics = topic
    for a in topics:
      ##Remove individual parts of a bigram from feature vector
      for w in a.split():
        if w != a:
          w = self.topic_index(w, dictionary)
          if w:
            dictionary = dictionary[:w] + dictionary[w+1:]

      a = a.replace(" ", "_")
      a = self.topic_index(a, dictionary)
      dictionary = dictionary[:a] + dictionary[a+1:]

    ##print len(dictionary)
    ##print len(coefs)

    m = 1
    while (m != 0 and len(coefs) > 0):
      maxc = max(coefs)
      minc = min(coefs)

      if abs(minc) > maxc:
        m = minc
      else:
        m = maxc

      f.write(str(dictionary[coefs.index(m)]) + " : " + str(m) + "\n")
      coefs.remove(m)

    f.close()

  def topic_index(self, topic, dictionary):
    try:
      return dictionary.index(topic)
    except:
      return False

  def topic_train(self, features, topics, dictionary):
    features = np.array(features)

    labels = np.array([0] * len(features))
    topic_i = []
    print len(features[0])
    for a in topics:
      ##Remove individual parts of a bigram from feature vector
      for w in a.split():
        if w != a:
          w = self.topic_index(w, dictionary)
          if w:
            topic_i.append(w)

      a = a.replace(" ", "_")
      temp = a
      a = self.topic_index(a, dictionary)

      topic_i.append(a)
      for i in range (0, len(features)):
        if features[i][a] == 1:
          labels[i] = 1

    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, topic_i, True)
    features = features[:,feat_i]

    print len(features[0])

    train_i = np.arange(len(features))
    validate_i = np.random.choice(train_i, int(len(features)*(0.5)), False)
    train_i = np.setdiff1d(train_i, validate_i, True)

    train_feat = features[train_i]
    validate_feat = features[validate_i]

    train_lab = labels[train_i]
    validate_lab = labels[validate_i]

    log = linear_model.LogisticRegression()
    log.fit(train_feat, train_lab)
    probs = np.array(log.predict_proba(validate_feat))[:,[1]]

    c = 0
    n = 0
    for i in range(0, len(validate_feat)):
      if validate_lab[i] == 1:
        c += probs[i]
        n += 1
    c = c/n

    self.write_model(log, topics, dictionary)

    return [log, c]

  def predict_topic_proba(self, features, topics, log, c, dictionary):
    features = np.array(features)

    labels = np.array([0] * len(features))
    topic_i = []
    for a in topics:
      ##Remove individual parts of a bigram from feature vector
      for w in a.split():
        if w != a:
          w = self.topic_index(w, dictionary)
          if w:
            topic_i.append(w)

      a = a.replace(" ", "_")
      a = self.topic_index(a, dictionary)
      topic_i.append(a)
      for i in range (0, len(features)):
        if features[i][a] == 1:
          labels[i] = 1

    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, topic_i, True)
    features = features[:,feat_i]

    predictions = []
    probs = log.predict_proba(features)
    for i in range(0, len(features)):
      if labels[i] == 1:
        predictions.append(1.0)
      else:
        if float(probs[i][1]/c) > 1:
          predictions.append(1.0)
        else:
          predictions.append(float(probs[i][1]/c))

    return predictions

  def write_topic_features(self, trainfile, testfile, dictfile, topicfile):
    rd = Read_Data()

    train = rd.read_features(trainfile, verbose=True)
    train_features = train[0]
    train_labels = train[1]

    test = rd.read_features(testfile, verbose=True)
    test_features = test[0]
    test_labels = test[1]

    dictionary = rd.read_dictionary(dictfile)

    topics = rd.read_topics(topicfile)

    trainoutfile = trainfile.replace('_features', '_topic_features')
    testoutfile = testfile.replace('_features', '_topic_features')

    train_topic_feats = [train_labels]
    test_topic_feats = [test_labels]
    for topic in topics:
      print topic
      a = self.topic_train(train_features, topic, dictionary)
      log = a[0]
      c = a[1]
      train_topic_feats.append(self.predict_topic_proba(train_features, topic, log, c, dictionary))
      test_topic_feats.append(self.predict_topic_proba(test_features, topic, log, c, dictionary))

    print len(train_topic_feats[0])
    f = open(trainoutfile, 'w')
    for j in range(0, len(train_topic_feats[0])):
      for i in range(0, len(train_topic_feats)):
        f.write(str(train_topic_feats[i][j]))
        f.write(" ")
      f.write("\n")
    f.close()

    f = open(testoutfile, 'w')
    for j in range(0, len(test_topic_feats[0])):
      for i in range(0, len(test_topic_feats)):
        f.write(str(test_topic_feats[i][j]))
        f.write(" ")
      f.write("\n")
    f.close()