import os, json, re, string, pandas, numpy, pickle
from pathlib import Path
from keras import losses #used for compiling models
from tensorflow.keras import models
from keras.models import Sequential
from keras.models import load_model
from keras.models import model_from_json
from keras.layers import Activation, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelBinarizer 


# Path to directory containing all training data
localPath = os.path.dirname(os.path.abspath(__file__))
path_to_json = localPath + "\\..\\Sample Data\\"
tokenizer = Tokenizer(num_words=15000)
trainTagsArr = []

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

    global trainTagsArr

    LABELS = "category"
    train_size = int(len(data) * .8)
    
    train_text = data['text'][:train_size]
    train_tags = data[LABELS][:train_size]

    test_text = data['text'][train_size:]
    test_tags = data[LABELS][train_size:]

    trainTagsArr = train_tags

    #print(len(set(data['category'])))
    # Dyamically set the number of LABELS
    num_labels = len(set(data[LABELS]))
    vocab_size = 15000
    batch_size = 100

    #tokenizer = Tokenizer(num_words=vocab_size)
    tokenizer.fit_on_texts(train_text)

    x_train = tokenizer.texts_to_matrix(train_text, mode='tfidf')
    x_test = tokenizer.texts_to_matrix(test_text, mode='tfidf')

    encoder = LabelBinarizer()
    encoder.fit(train_tags)
    y_train = encoder.transform(train_tags)
    y_test = encoder.transform(test_tags)

    myModel = buildModel(num_labels, vocab_size, x_train, y_train, batch_size)

    score = myModel.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)

    print('Test Accuracy: ', score[1])
    print("Score: ", score) #[2.1682879958161054, 0.6556665238172553]
    return myModel

def saveTrainedModel(trainedModel, tokenizer):
    """Saving trained model to HDF5 file, and saving tokenizer to local directory.
    PARAMETER - trained model with tokenizer
    RETURN - NULL"""

    #Save model and tokenizer
    trainedModel.save('trainedModel.h5')

    #Saves tokenizer (ie. Vocabulary)
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved model to disk.")
    return

def loadTrainedModel(modelPath):
    """Loads a previously trained and saved model to local directory into memory.
    PARAMETER - path of where to load model
    RETURN - loaded trained model"""

    global tokenizer

    loadedTrainedModel = load_model(modelPath)
    #Loads tokenizer (ie. Vocabulary)
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    loadedTrainedModel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print("Loaded model from disk.")
    return loadedTrainedModel

#Currently does more than just buildModel. Needs refactoring
def buildModel(num_labels, vocab_size, x_train, y_train, batch_size):
    """Loads the a previously trained AI model that's located in MODEL_PATH
    if exists, otherwise builds the model from scratch.
    PARAMETER - the number of labels (num_labels), the size of the vocabulary
        (vocab_size), x_train, y_train, and the rate of the learning (batch_size)
    RETURN - the built model"""

    global tokenizer
    
    #Make uniform string for paths match the ones in saveTrainedModel and loadTrainedModel functions
    MODEL_PATH = Path(localPath + "/trainedModel.h5")
    if (MODEL_PATH.exists()):#Load file
        myModel = loadTrainedModel(str(MODEL_PATH))
        return myModel
    else:#Build model and save
        myModel = Sequential()
        #Create layers
        myModel.add(Dense(512, input_shape=(vocab_size,)))
        myModel.add(Activation('relu'))
        myModel.add(Dropout(0.3))
        myModel.add(Dense(num_labels))
        myModel.add(Activation('softmax'))
        myModel.summary()
        myModel.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
        #Unused variable 'history'
        history = myModel.fit(x_train, y_train, batch_size=batch_size, epochs=15, verbose=1, validation_split=0.1)#Train
        
        myModel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        saveTrainedModel(myModel, tokenizer)
        return myModel

def predictCategory(myModel, userInput):
    """With given input from user, predicts what category.
    PARAMETERS - an AI model as a keras model and user input as
        text to categorize (predict to)
    RETURN - predicted label for userInput"""

    #These are used to check the predicted label. MUST BE ORGANIZED same way as encoded
    #labels = numpy.array(['msoffice', 'outlook', 'windows', 'xbox'])

    labels = numpy.array(trainTagsArr)
    matrixedInput = tokenizer.texts_to_matrix(userInput, mode='tfidf')
    prediction = myModel.predict(numpy.array(matrixedInput))
    #prediction label is a string matching the prediction within the 'labels' array
    predictedLabel = labels[numpy.argmax(prediction[0])]
    return predictedLabel

#This should be part of the database class
def insertIntoDatabase(contents):
    """Inputs given contents to the set database.
    PARAMETERS - contents as an array for either a string
        or a string and the predicted category.
    RETURN - NULL"""

    print("insertIntoDatabase() not yet implemented")
    return

def setDatabase(param1, param2, param3, param4):
    """Sets preferred database for the AI to fetch and insert to.
    PARAMETERS - 
    RETURN - NULL"""

    return

def recieveString():
    """Waits for input, returns what user inputted.
    PARAMETER - NULL
    RETURN - string"""

    print("Enter your response: ")
    myString = input()
    if myString is None:
        myString = ""

    return myString



#Program starts here
data = load_training_data(path_to_json)
trainedModel = train_model(data)
while(True):
    content = recieveString()#Get input from console
    prediction = predictCategory(trainedModel, str(content))
    print(prediction)

exit()#Program stops here
