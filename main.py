import get_restaurant_review_data as rd

rd = rd.Get_restaurant_reviews()

path = "scripts/data_files"
city = "Phoenix"
category = "Mexican"

rd.get_restaurant_reviews(path, city, category, True, True)