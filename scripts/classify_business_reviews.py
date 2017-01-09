import json, os

business_file = 'data_files/yelp_academic_dataset_business.json'
review_file = 'data_files/yelp_academic_dataset_review.json'
business_review_file = 'data_files/test_data.json'
city = "Phoenix"
category = "Mexican"
max_business_records = 5
max_review_records = 10
business_records = []

with open(business_file) as json_data:
    for line in json_data:
      if json.loads(line)['city'] == city and category in json.loads(line)['categories']:
        business_records.append(json.loads(line))
        if len(business_records) == max_business_records:
          break;

words = [data['business_id'] for data in business_records]
print words

if os.path.isfile(business_review_file):
  os.remove(business_review_file)

with open(review_file) as json_data:
    for word in words:
      word_count = 0
      for line in json_data:
        if json.loads(line)['business_id'] == word:
          word_count += 1
          with open(business_review_file, 'a') as f:
              json.dump(json.loads(line), f)
              f.write('\n')
          if word_count == max_review_records:
            break;
