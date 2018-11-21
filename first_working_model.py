import os, json, re, string, pandas, numpy, pickle
from pathlib import Path
from tensorflow.keras import models
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Activation, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelBinarizer 


# Path to directory containing all training data
localPath = os.path.dirname(os.path.abspath(__file__))
path_to_json = localPath + "\\Sample Data\\"

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

def train_model(data):
    """From loaded data, train model based on text (content) and LABELS.
    PARAMETER - data to train and test from
    RETURN - trained model
    """

    LABELS = "subcategory"
    train_size = int(len(data) * .8)
    
    train_text = data['text'][:train_size]
    train_tags = data[LABELS][:train_size]

    test_text = data['text'][train_size:]
    test_tags = data[LABELS][train_size:]

    #print(len(set(data['category'])))
    # Dyamically set the number of LABELS
    num_labels = len(set(data[LABELS]))
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

    myModel = buildModel(num_labels, vocab_size, x_train, y_train, batch_size)

    with open('tokenizer.pickle', 'wb') as handle:#Saves tokens to help for speeding up next run
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    score = myModel.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)

    print('Test Accuracy: ', score[1])
    print("Score: ", score) #[2.1682879958161054, 0.6556665238172553]
    return

#Currently does more than just buildModel. Needs refactoring
def buildModel(num_labels, vocab_size, x_train, y_train, batch_size):
    """Loads the a previously trained AI model that's located in MODEL_PATH
    if exists, otherwise builds the model from scratch.
    PARAMETER - the number of labels (num_labels), the size of the vocabulary
        (vocab_size), x_train, y_train, and the rate of the learning (batch_size)
    RETURN - the built model"""
    
    MODEL_PATH = Path(localPath + "/testModel.h5")
    print("Model path: " + str(MODEL_PATH))
    print("Result of isFile: " + str(os.path.isfile(MODEL_PATH)))
    if (MODEL_PATH.exists()):#Returns true if file exists
        print("File exits. Loaded previous model.")
        model = load_model(str(MODEL_PATH))
        return model
    else:#Build model
        model = Sequential()
        #Create layers
        model.add(Dense(512, input_shape=(vocab_size,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.3))
        model.add(Dense(num_labels))
        model.add(Activation('softmax'))
        model.summary()
        model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
        #Unused variable 'history'
        history = model.fit(x_train, y_train, batch_size=batch_size, epochs=30, verbose=1, validation_split=0.1)
        model.save("testModel.h5")
        return model

def predictCategory(model, userInput):
    """With given input from user, predicts what category.
    PARAMETERS - an AI model as a keras model and user input as
        text to categorize (predict to)
    RETURN - updated model"""

    print("predictCategory() not yet implemented")
    return model

def insertIntoDatabase(contents):
    """Inputs given contents to the set database.
    PARAMETERS - contents as an array for either a string
        or a string and the predicted category.
    RETURN - NULL"""

    print("insertIntoDatabase() not yet implemented")
    return



#Program starts here
data = load_training_data(path_to_json)
train_model(data)

exit()#Program stops here
