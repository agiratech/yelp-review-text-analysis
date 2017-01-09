import get_restaurant_review_data as rd
import data_pre_processing as dpp
rd = rd.Get_restaurant_reviews()
dpp = dpp.Preprocessing()
path = "data_files"
city = "Phoenix"
category = "Mexican"
topic = "./"+path+"/topic.txt"

dataFile = rd.get_restaurant_reviews(path, city, category, True, True)
dpp.process_anchors(dataFile, topic)