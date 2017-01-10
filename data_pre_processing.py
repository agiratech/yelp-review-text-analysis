import json, re
from Read_and_write import read_and_write_data
from nltk.tokenize import word_tokenize
from collections import Counter

rwd = read_and_write_data.Read_Data()

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

        data["text"] = review
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