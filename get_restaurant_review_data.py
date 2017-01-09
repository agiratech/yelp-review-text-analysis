import json, time, os

# get reviews for perticular retaurant
class Get_restaurant_reviews:

  def get_review_file(self, restaurant_bIds, path, review_flag):
    infile = path+'/yelp_academic_dataset_review.json'
    outfile = '(restaurant)selected_review.json'
    reviews_count = 0
    with open(path+'/yelp_academic_dataset_review.json') as json_data, open(outfile,'w') as file:
      for line in json_data:
        review_line = json.loads(line)
        if review_line['business_id'] in restaurant_bIds:
          json.dump({'business_id':review_line['business_id'],  \
                      'user_id': review_line['user_id'], 'stars':review_line['stars'], \
                      'text':review_line['text']}, file)
          file.write('\n')
          reviews_count += 1
          if review_flag == True:
            if reviews_count == 1000:
              break;
    return outfile, reviews_count

  def get_restaurant_reviews(self, path, city, category, business_flag=False, review_flag=False):
    start = time.time()
    business_ids = []
    ids_count = 0
    with open(path+'/yelp_academic_dataset_business.json') as json_data:
      for line in json_data:
        if city == 'None' and category in json.loads(line)['categories']:
          business_ids.append(json.loads(line)['business_id'])
        if json.loads(line)['city'] == city and category in json.loads(line)['categories']:
          business_ids.append(json.loads(line)['business_id'])
        if business_flag:
          if len(business_ids) == 5:
            break;
    outfile, reviews_count = self.get_review_file(business_ids, path, review_flag)

    end = time.time()
    print 'There are {0} {1} restaurants '.format(len(business_ids), category)
    print 'There are {0} reviews on selected businesses'.format(reviews_count)
    print 'All data saved to {0}'.format(outfile)
    print 'Entire process took {0}'.format(end-start)

    return outfile