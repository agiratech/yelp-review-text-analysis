
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