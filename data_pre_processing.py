import json, re
from Read_and_write import read_and_write_data
from nltk.tokenize import word_tokenize

rwd = read_and_write_data.Read_Data()

class Preprocessing:

  # Underscores multiword topics and optionally removes words
  # in size-n window around topics to increase conditional independence
  # of topics and the text.  Default window size is 0

  def process_anchors(self, infile, topicfile, window_size=0):
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