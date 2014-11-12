import os
import pdb
import random

import numpy as np
import nltk
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

feature_key = ['search','retrieval','retrieval_from_search','preview','preview_from_search','rs_ratio','add_to_my_list','email','print','export_easylib']

def main():
    satispath = '/home/ec2-user/UMMDP14/python_scripts/satis/'
    unsatispath = '/home/ec2-user/UMMDP14/python_scripts/unsatis/'
    satisfile = open(satispath + 'satis_2014-10', 'rU')
    unsatisfile =  open(unsatispath + 'unsatis_2014-10', 'rU')
    satistrain, satistest = get_featureset(satisfile, True)
    unsatistrain, unsatistest = get_featureset(unsatisfile, False)
    satisfile.close()
    unsatisfile.close()
    #train
    train_total = satistrain + unsatistrain
    test_total = satistest + unsatistest
    Cs = [0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 500, 1000]
    '''for theC in Cs:
        classifier = LinearSVC(C=theC, verbose=1)
        svm_classifier = SklearnClassifier(classifier).train(train_total[:int(len(train_total)/2)])
        accuracy = nltk.classify.accuracy(svm_classifier, train_total[int(len(train_total)/2):])  #test_total)
        print "using C=: " + str(theC) + ' accuracy: {0:.2f}%'.format(100*accuracy)
        print 'parameters: ' + np.array_str(classifier.coef_)
    '''
    classifier = LinearSVC(C=0.01, verbose=1)
    svm_classifier = SklearnClassifier(classifier).train(train_total)
    accuracy = nltk.classify.accuracy(svm_classifier, test_total)
    print "final using C= 0.01 " + ' accuracy: {0:.2f}%'.format(100*accuracy)
    print 'parameters: ' + np.array_str(classifier.coef_)

    return

def get_featureset(infile, isSatis):
    filelines = infile.read().split('\n')
    sampleindices = random.sample(range(0, len(filelines)), int(len(filelines)*0.7))
    sampleindicesdict = dict()
    for index in sampleindices:
        sampleindicesdict[index] = True

    trainset = []
    testset = []
    
    for i in range(0, len(filelines)-1): #skip the last ''
        feature = filelines[i].split(',')
        featuredict = {}
        feature_val = feature[2:-1]
        if (len(feature_val) != len(feature_key)):
            print 'error @ '
            continue

        for x in range(0,len(feature_key)):
            featuredict[feature_key[x]] = float(feature_val[x])
            
        if i in sampleindicesdict:
            trainset.append((featuredict, isSatis))
        else:
            #pdb.set_trace()
            testset.append((featuredict, isSatis))
        #featuredict.clear()
    
    #pdb.set_trace()
    return trainset, testset

main()
