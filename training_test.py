import os, json, re, string, nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

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
    train_labels = []

    for file in json_filelist:
        #print(file)
        with open(path_to_json + file) as json_file:
            data = json.load(json_file)
            for p in data:
                if(p['category'] == 'msoffice'):#Only from one category
                    train_texts.append(p['content'].lower())
                    train_labels.append(p['category'])

    return((train_labels, train_texts))

def tokenizeData(trainContents, trainLabels):
    """From the data in memory, tokenize the data into bigrams."""
    cleanData()
    bigrams = []
    token = list()
    counter = 0
    for docContents in trainContents:
        token += nltk.word_tokenize(docContents)
        bigrams = ngrams(token, 2)#Tokenize
    #For printing the most frequent bi-gram
    for key, value in Counter(bigrams).items():
        if value >= 250:
            print(key)
            counter += 1
            print("Found " + str(counter) + " having atleast 250")
    #print(Counter(bigrams))

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
labels, contents = load_training_data(path_to_json)
setupUniqueCategories(labels, unique_categories)
tokenizeData(contents, labels)

exit()#Program stops here

bigrams = [b for l in contents for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]

unigrams = []
for string in contents:
    unigrams.append(string.split())

print(unigrams)

