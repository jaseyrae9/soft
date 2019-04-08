from sklearn.datasets import fetch_mldata
from sklearn.neighbors import KNeighborsClassifier
from skimage import exposure
import cv2
import numpy as np
from keras.datasets import mnist
import os.path
import _pickle as cPickle
import gzip

def getKNN():

    pkl_filename = "pickle_model.pkl"  
    if(os.path.isfile(pkl_filename)):
        with open(pkl_filename, 'rb') as file:  
            pickle_model = cPickle.load(file)
            return pickle_model
    else:
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        data_train = []
        for x in X_train:
            y = x.reshape(1, 784)
            data_train.append(y.flatten())
      
       # print('data shape:' + str(data[0].shape))
        #data = data.shape(28,28)
        knn = KNeighborsClassifier(n_neighbors=1, algorithm='auto').fit(data_train, y_train)
        data_test = []
        for x in X_test:
            y = x.reshape(1, 784)
            data_test.append(y.flatten())
        print('Preciznost: ')
        print(knn.score(data_test, y_test))

        with open(pkl_filename, 'wb') as file:  
            cPickle.dump(knn, file)

        return knn

