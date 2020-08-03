# -*- coding: utf-8 -*-
"""deepCNN_food_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jnHMPr_TGrZjUqpsdwWRLUHrDSQnnoTb
"""

# Commented out IPython magic to ensure Python compatibility.
# Deep CNN food classification model

import os
import sys
import shutil
from PIL import Image
from lxml import etree as ET
from tqdm import tqdm
from copy import deepcopy
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from imgaug import augmenters as iaa
import glob
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D,GlobalAveragePooling2D
from keras.layers import LSTM, Input, TimeDistributed,Convolution2D,Activation
from keras.layers.convolutional import ZeroPadding2D
from keras.optimizers import RMSprop, SGD
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras import optimizers
from keras.preprocessing import sequence
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import load_model

from sklearn.preprocessing import LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

# Import the backend
from keras import backend as K
from tqdm import tqdm
from collections import Counter
import pandas as pd
import numpy as np
import os

print("modules imported...")
"""# Initialization"""

BASE_PATH = os.path.join(os.getcwd(), 'food-model-files') #'/kaggle/input/' 
# LABELS = ['rice', 'roti', 'dal', 'sabzi']
LABELS = ['rice', 'roti', 'dal', 'sabzi']
 
print("BASE_PATH {}".format(BASE_PATH))
"""# Building CNN Model"""

def get_alexnet(input_shape, nb_classes): 
    model = Sequential() 
    # Layer 1 
    model.add(Convolution2D(96, 11, 11, input_shape = input_shape, border_mode='same')) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2))) 
    # Layer 2 
    model.add(Convolution2D(128, 5, 5, border_mode='same')) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2),strides=2)) 
    # Layer 3 
    model.add(ZeroPadding2D((1,1))) 
    model.add(Convolution2D(384, 3, 3, border_mode='same')) 
    model.add(Activation('relu')) 
    # Layer 4 
    model.add(ZeroPadding2D((1,1))) 
    model.add(Convolution2D(192, 3, 3, border_mode='same')) 
    model.add(Activation('relu')) 
    # Layer 5 
    model.add(ZeroPadding2D((1,1))) 
    model.add(Convolution2D(128, 3, 3, border_mode='same')) 
    model.add(Activation('relu')) 
    model.add(MaxPooling2D(pool_size=(2, 2))) 
    # Layer 6 
    model.add(GlobalAveragePooling2D()) 
    model.add(Dense(4096, init='glorot_normal')) 
    model.add(Activation('relu')) 
    model.add(Dropout(0.5)) 
    # Layer 7 
    model.add(Dense(4096, init='glorot_normal')) 
    model.add(Activation('relu')) 
    model.add(Dropout(0.5)) 
    # Layer 8 
    model.add(Dense(nb_classes, init='glorot_normal')) 
    model.add(Activation('tanh')) 
    return model

"""# Loading data"""

def load_data():
    all_images = []
    # train_labels = [] 

        # for f in os.listdir(os.path.join(BASE_PATH, "Dataset", str(i))):
    for f in tqdm(glob.glob(os.path.join(BASE_PATH, "*.jpg"))):
        img = cv2.imread(f, cv2.IMREAD_COLOR)       
        img = cv2.resize(img, (227, 227))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        all_images.append((f[f.rfind('/')+1:], img))


    # plt.imshow(all_images[50][1])
    # plt.title(all_images[50][0])
    # plt.show()

    all_labels = []
    with open(os.path.join(BASE_PATH, 'new_annotations_onehot_1.txt'), 'r') as f:
        
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            
            fname, lab = line.split(' ')
            print('fname {} lab {}'.format(fname, lab))
            all_labels.append((fname, lab))

    # print(len(all_labels))
    # print(all_labels[50])

    for i in all_labels:
        filename = i[0]

    # Mapping between images and labels
    lnames = [f[0] for f in all_labels]
    for l in all_images:
        if l[0] not in lnames:
            print(l[0])
    to_remove = ['782.jpg', '803.jpg', '615.jpg', '880.jpg', '671.jpg', '607.jpg', '1146.jpg'] 
    all_images_filter = []
    for i in tqdm(all_images):
        if i[0] not in to_remove:
            all_images_filter.append(i)


    dataset = []
    df1 = pd.DataFrame(all_labels)
    df1.rename(columns={0: 'filename', 1: 'label'}, inplace=True)

    df2 = pd.DataFrame(all_images_filter)
    df2.rename(columns={0: 'filename', 1: 'image'}, inplace=True)

    x = df1.merge(df2, on='filename')
    dataset = x[['image', 'label']]
    train_images, test_images, train_labels, test_labels = train_test_split(dataset['image'], dataset['label'], test_size=0.2, shuffle=True)
    train_images, test_images, train_labels, test_labels = list(train_images), list(test_images), list(map(float, list(train_labels))), list(map(float, list(test_labels)))
    return train_images, test_images, train_labels, test_labels


"""# CNN for feature extraction"""

def train_cnn(train_images, test_images, train_labels, test_labels):
    alexnet = get_alexnet((227,227,3),15)
    alexnet.summary()

    alexnet.compile(loss='categorical_crossentropy', optimizer=RMSprop(),metrics=['accuracy'])
    X_normalized = np.array(np.asarray(train_images) / 255.0 - 0.5 )
    X_normalized_test = np.array(np.asarray(test_images) / 255.0 - 0.5 )

    # label_binarizer = LabelBinarizer()
    # y_one_hot = label_binarizer.fit_transform(train_labels)
    # y_one_hot_test = label_binarizer.fit_transform(test_labels)
    # print(y_one_hot[0])

    y_one_hot = np.zeros(shape=(len(train_labels), 15))
    y_one_hot_test = np.zeros(shape=(len(test_labels), 15))

    for i in range(len(train_labels)):
        y_one_hot[i][int(train_labels[i])-1] = 1
    for i in range(len(test_labels)):
        y_one_hot_test[i][int(test_labels[i])-1] = 1


    alexnet.fit(X_normalized, y_one_hot, batch_size=5, epochs=2,verbose=1, validation_data=[X_normalized_test,y_one_hot_test])
    # alexnet_json = alexnet.to_json()
    # with open(model_path, 'r') as f:
    #     f.write(alexnet_json)
    alexnet.save(os.path.join(BASE_PATH, 'alexnet_food_model.h5'))

"""# Extending CNN model to RF"""

def load_saved_model(model_path):
    return load_model(model_path)

def cnn_extension_RF(alexnet, isPresent=True, train_images=None, test_images=None, train_labels=None, test_labels=None):
    layer_name = 'dense_1'
    FC_layer_model = Model(inputs= alexnet.input,
                                    outputs=alexnet.get_layer(layer_name).output)

    # assert (len(train_images) == np.asarray(train_images).shape[0])
    if isPresent == False:
        i=0
        features = np.zeros(shape=(len(train_images), 4096))
        for _img in tqdm(train_images):
            # img = cv2.imread(img_path, cv2.IMREAD_COLOR)    
            # img = cv2.resize(img, (227, 227))
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = np.expand_dims(_img, axis=0)
            FC_output = FC_layer_model.predict(img)
            features[i]=FC_output
            i+=1

        #Save the features of the train images to use it in future.
        np.save(os.path.join(BASE_PATH, 'features'), features)

        feature_col=[]
        for i in range(4096):
            feature_col.append("f_"+str(i))
            i+=1
        with open(os.path.join(BASE_PATH, 'feature_col.txt'), 'w') as f:
            for i in feature_col:
                f.write(i+'\n')
        with open(os.path.join(BASE_PATH, 'train_labels.txt'), 'w') as f:
            for i in train_labels:
                f.write(i+'\n')           
    else:
        feature_col = []
        with open(os.path.join(BASE_PATH, 'feature_col.txt'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                l = line.rstrip('\n')
                feature_col.append(l)

        train_labels = []
        with open(os.path.join(BASE_PATH, 'train_labels.txt'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                l = line.rstrip('\n')
                train_labels.append(float(l))        
        train_label_ids = [np.uint(tl) for tl in train_labels]
        features = np.load(os.path.join(BASE_PATH, 'features.npy'))       
        train_features=pd.DataFrame(data=features,columns=feature_col)
        feature_col = np.array(feature_col)
        print("Training features read...")

    """## Random Forest Classifier"""

    rf = RandomForestClassifier(n_estimators = 12, random_state = 24, max_features=10)

    rf.fit(train_features, train_label_ids)
    print("features fit into RF...")
    if isPresent == False:
        i=0
        features_test=np.zeros(shape=(len(test_images), 4096))
        for _img in tqdm(test_images):
            # img = cv2.imread(img_path, cv2.IMREAD_COLOR)    
            # img = cv2.resize(_img, (227, 227))
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = np.expand_dims(img, axis=0)
            FC_output = FC_layer_model.predict(img)
            features_test[i]=FC_output
            i+=1
        np.save(os.path.join(BASE_PATH, 'features_test'), features_test)
        with open(os.path.join(BASE_PATH, 'test_labels.txt'), 'w') as f:
            for i in test_labels:
                f.write(i+'\n') 
    # test_images[313].shape
    else:
        features_test = np.load(os.path.join(BASE_PATH, 'features_test.npy'))
        test_labels = []
        with open(os.path.join(BASE_PATH, 'test_labels.txt'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                l = line.rstrip('\n')
                test_labels.append(float(l))
        test_label_ids = [np.uint(tl) for tl in test_labels]        


    test_features=pd.DataFrame(data=features_test,columns=feature_col)
    feature_col = np.array(feature_col)

    # print('Test Features Shape:', test_features.shape)
    # print('Test Labels Shape:', np.asarray(test_label_ids).shape)

    """### Classification by Random Forest"""

    #Feed the features of the test images to Random Forest Classifier to predict its class
    predictions = rf.predict(test_features)

    accuracy=accuracy_score(predictions , test_label_ids)
    print('Accuracy:', accuracy*100, '%.')
    return FC_layer_model, rf, feature_col

def dec2bin(num):
    return bin(num)

def get_classes(prediction):
    class_decodings = {"rice": 0b1000, "roti": 0b0100, "dal": 0b0010, "sabzi": 0b0001}
    bin_pred = int(dec2bin(prediction), 2)
    classes = []
    for i, j in class_decodings.items():
        if ((bin_pred) & j) == j:
            classes.append(i)
    return classes

"""## Predictions on Images"""
def get_predictions(image):
    print("In get_predictions()...")
    alexnet = load_saved_model(os.path.join(BASE_PATH, 'alexnet_food_model.h5'))
    # train_x, test_x, train_y, test_y = load_data()
    FC_layer_model, rf, feature_col = cnn_extension_RF(alexnet) #, isPresent=False, train_images=train_x, test_images=test_x, train_labels=train_y, test_labels=test_y)
    FC_output = FC_layer_model.predict(image)
    image_features=pd.DataFrame(data=FC_output, columns=feature_col)
    predictions = rf.predict(image_features)
    return predictions

def predict_on_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (227, 227))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # plt.imshow(img)
    img = np.expand_dims(img, axis=0)
    predictions = get_predictions(img)
    
    return get_classes(predictions[0])

if __name__ == '__main__':
    image_path = os.path.join(BASE_PATH, 'test_image_3.png')
    results = predict_on_image(image_path) 
    print("It's ", results)