import os, json, re, string
from string import punctuation

# Path to directory containing all training data
path_to_json = os.path.dirname(os.path.abspath(__file__))
path_to_json += "\\Sample Data\\"
#path_to_json = 'C:\\Users\\Alex\\virtualenvironment\\421\\Sample Data\\'


def load_training_data(data_path):
    
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
                train_texts.append(p['content'].lower())
                train_labels.append(p['category'])

    return((train_labels, train_texts))

labels, contents = load_training_data(path_to_json)

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


unique_categories = []

for x in labels:
    if x not in unique_categories:
        unique_categories.append(x)
#print(unique_categories)

for x in contents:
    strip_punctuation(x)

bigrams = [b for l in contents for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]

print(bigrams)

