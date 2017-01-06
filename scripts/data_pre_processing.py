import nltk,re

# strip the suffix # stemming
def stem(word):
  regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|s|es|ment)?$'
  stem, suffix = re.findall(regexp, word)[0]
  return stem

raw = "There's a lot going on in this pipeline. To understand it properly, it helps to be clear about the type of each variable that it mentions. We find out the type of any Python object x using type(x), e.g. type(1) is <int> since 1 is an integer."

punctuation = re.compile(r'''[-.?!,":;()<>|0-9]''')
stop_words=['a','an' ,'the','of', 'is', 'this', 'in', 'there', 'on','it', 'to',"there's"]

# punctuation and numbers to be removed
# convert lower
# removing stop words
# tokenized
words = [stem(w).lower() for w in nltk.word_tokenize(punctuation.sub("", raw)) if w.lower() not in stop_words]
print words



