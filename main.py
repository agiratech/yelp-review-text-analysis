import numpy as np
import get_restaurant_review_data as rrd
from Read_and_write import read_and_write_data as rwd
import data_pre_processing as dp
import partition_reviews as pr

rrd = rrd.Get_restaurant_reviews()
dpp = dp.Preprocessing()
pr = pr.Partition_Reviews()
topic = rwd.Write_topics()
rd = rwd.Read_Data()

path = "data_files"
city = "Phoenix"
category = "Mexican"
topicfile = "topic.txt"
indexfile = "indices.txt"
dictfile = "dictionary.txt"

datafile = rrd.get_restaurant_reviews(path, city, category, True, True)
datafile = dpp.process_topics(datafile, topicfile)
print "555555", datafile

num_reviews = pr.count_reviews(datafile)
pr.generate_set_indices(num_reviews)
print "6666666", datafile
pr.partition_reviews(datafile, indexfile)

trainfile = 'train'+datafile[datafile.index('_'):]
validatefile = 'validate'+datafile[datafile.index('_'):]

dpp.write_dictionary(trainfile, dictfile)

trainfile = dpp.write_features(trainfile, dictfile)
validatefile = dpp.write_features(validatefile, dictfile)

topic.write_topic_features(trainfile, validatefile, dictfile, topicfile)

train_a = rd.read_features('train_topic_features.txt')
train_a_feats = np.array(train_a[0])
train_a_labels = np.array(train_a[1])

validate_a = rd.read_features('validate_topic_features.txt')
validate_a_feats = np.array(validate_a[0])
validate_a_labels = np.array(validate_a[1])

print "topic features done"