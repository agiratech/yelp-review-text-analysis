# Yelp review text analysis
Yelp review text analysis using natural language processing

# Problem Statement
How well can you guess a review's rating from its text alone?

# Initial Objective
* Storing/grouping of required data from original data sets

  Storing/classifying business reviews based on restaurant type (Mexican, Italian, Indian) and city (Chennai, Pittsburgh) as new JSON file.To do this, we have to combine and classify the two original data sets of Yelp 

* Data Pre-Processing includes
  Remove non-writable characters.
  Strip extra white spaces.
  Lower case.
  Remove punctuation
  Remove numbers
  Stemming
  Stop words removal

* Data Partitions (3 subsets randomly)
  Split entire data sets into two or three groupings based on random, so we can easily cross check / validate groupings data whether it’s valid or not.
  
* Build dictionary using one partition
  Based on one grouping, build bag of words as dictionary
  
* Features build using partitions and dictionary
  Based on partitions and dictionary, cross check dictionary word with review text and to do star rating calculation also.Then combine calculation in matrix format with value either 0 or 1
  
* Build final features
  Build final feature using nltk linear model and probability approach
  
* Need to do later
