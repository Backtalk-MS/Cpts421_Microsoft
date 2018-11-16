import os, json, re, string, pandas
from tensorflow.keras import models
from keras.preprocessing.text import Tokenizer

# Path to directory containing all training data
path_to_json = os.path.dirname(os.path.abspath(__file__))
path_to_json += "\\Sample Data\\"

def load_training_data(data_path):
    """Reads the scrapped json documents stored on the local machine and load
    contents and its categories into data."""
    json_filelist = os.listdir(path_to_json)

    # Load the training data
    # For every json file in the directory, load up the contents of it and
    # the labels
    train_texts = []
    train_labels = ["text", "category", "subcategory"]

    for file in json_filelist:
        #print(file)
        with open(path_to_json + file) as json_file:
            data = json.load(json_file)
            for p in data:
                train_texts.append((p['content'], p['category'], p['subcategory']))
    data = pandas.DataFrame.from_records(train_texts, columns=train_labels)                
    print(data)
    return #((train_labels, train_texts))


def vectorizeData(unigrams, bigrams):
    uniVectors = []
    biVectors = []
    return uniVectors, biVectors
# Function to strip punctuation
def strip_punctuation(s):
    """Helper function to strip the unnecessary punctuation to
    get bigrams of WORDS only."""
    return ''.join(c for c in s if c not in string.punctuation)

unique_categories = []
def setupUniqueCategories(labels, categories):
    """Store categories of each entry according to the categories."""
    for x in labels:
        if x not in categories:
            categories.append(x)
    #print(unique_categories)

def cleanData():
    """Calls helper function for each entry and strips the punctuation."""
    for x in range(len(contents)):
        contents[x] = strip_punctuation(contents[x])

#Program starts here
unigrams = []
bigrams =[]
unigramVectors = []
bigramVectors = []
load_training_data(path_to_json)
#labels, contents = load_training_data(path_to_json)
#setupUniqueCategories(labels, unique_categories)
#unigramVectors, bigramVectors = vectorizeData(unigrams, bigrams)

exit()#Program stops here
