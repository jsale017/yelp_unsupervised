import pandas as pd
import numpy as np
import nltk
from gensim.models import Word2Vec
from gensim.parsing import PorterStemmer
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# stem and lemmatize objects
stem = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


# takes a token (str) and a model (object).... Word2Vec in this case
# returns a word embedding or an appropriately sized vector of zeroes depending on the models keys
def embed(word, model):
    if word in model.key_to_index:
        return model[word]
    else:
        return np.zeros(model.vector_size)


# takes a review and recompiles it to a review with only stems of non-homonyms, excluding stop words
def process_text(text):
    tokens = word_tokenize(text)
    w: str
    tokens = [w for w in tokens if
              w not in stop_words]  # list comprehension of tokenized but checks for stop words and filters them out
    # tokens = [stem.stem(w) for w in tokens]
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    text = ' '.join(tokens)
    return text


# read the reviews in
reviews = pd.read_csv('./data/under-sample.csv')

# clean
reviews_clean = pd.DataFrame(reviews.text.str.lower().str.strip())
reviews_clean = pd.DataFrame(reviews_clean.text.str.replace(r'/[^a-zA-Z0-9]/g', ''))
reviews_clean = pd.DataFrame(reviews_clean.text.str.replace(r'[^a-zA-Z\s]', ''))
reviews_clean = pd.DataFrame(reviews_clean.text.str.replace(r'[^\w\d\s]', ''))

# tokenize and send to .npy
tokenized = [word_tokenize(w) for w in tqdm(reviews_clean.text.apply(lambda review: process_text(review)), total=len(reviews_clean))]
tokenized = np.array(tokenized, dtype=object)
with open('data/tokenized.npy', 'wb') as file:
    np.save(file, tokenized)

# instantiate a Word2Vec with our embeddings and send to npy, tuning would require knowledge of optimization,
# we'll utilize default params here
w2v = Word2Vec(sentences=tokenized).wv

# embed loop
embeddings = []
for review in tqdm(tokenized):
    embedded = [embed(w, w2v) for w in review]
    rev_embedding = np.mean(embedded if len(embedded) > 0 else [np.zeros(w2v.vector_size)], axis=0)
    embeddings.append(rev_embedding)

embeddings = np.array(embeddings)
with open('data/embeddings.npy', 'wb') as file:
    np.save(file, embeddings)
