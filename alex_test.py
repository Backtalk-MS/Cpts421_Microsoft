import os, json, re, string, pandas, numpy, pickle
from tensorflow.keras import models
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelBinarizer 


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
    data = data.sample(frac=1).reset_index(drop=True)            
    #print(data)
    return data


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

def tokenizeData(data):
    train_size = int(len(data) * .8)
    
    train_text = data['text'][:train_size]
    train_tags = data['category'][:train_size]

    test_text = data['text'][train_size:]
    test_tags = data['category'][train_size:]

    #print(len(set(data['category'])))
    # Dyamically set the number of categories
    num_labels = len(set(data['category']))
    vocab_size = 15000
    batch_size = 100

    tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(train_text)

    x_train = tokenizer.texts_to_matrix(train_text, mode='tfidf')
    x_test = tokenizer.texts_to_matrix(test_text, mode='tfidf')

    encoder = LabelBinarizer()
    encoder.fit(train_tags)
    y_train = encoder.transform(train_tags)
    y_test = encoder.transform(test_tags)

    model = Sequential()
    model.add(Dense(512, input_shape=(vocab_size,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    model.summary()

    model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=30, verbose=1, validation_split=0.1)

    model.model.save('test_model.h5')

    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)

    print('Test Accuracy: ', score[1])
    #print(y_train)
    return

#Program starts here
unigrams = []
bigrams =[]
unigramVectors = []
bigramVectors = []
data = load_training_data(path_to_json)
tokenizeData(data)
#labels, contents = load_training_data(path_to_json)
#setupUniqueCategories(labels, unique_categories)
#unigramVectors, bigramVectors = vectorizeData(unigrams, bigrams)

exit()#Program stops here
