import get_restaurant_review_data as rd
import data_pre_processing as dpp
import partition_reviews as pr

rd = rd.Get_restaurant_reviews()
dpp = dpp.Preprocessing()
pr = pr.Partition_Reviews()

path = "data_files"
city = "Phoenix"
category = "Mexican"
topic = "topic.txt"
indexfile = "indices.txt"

dataFile = rd.get_restaurant_reviews(path, city, category, True, True)
dataFile = dpp.process_anchors(dataFile, topic)
print "555555", dataFile

num_reviews = pr.count_reviews(dataFile)
pr.generate_set_indices(num_reviews)
print "6666666", dataFile
pr.partition_reviews(dataFile, indexfile)