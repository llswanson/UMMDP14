import threading
import glob
import sys,os
import pdb
import random
from collections import OrderedDict

import numpy as np
import nltk
from sklearn import cross_validation
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

feature_key = ['search','retrieval','retrieval_from_search','preview','preview_from_search','rs_ratio','add_to_my_list','email','print','export_easylib']

def train2years(storeposfix, openposfix):
    output = open('classify/classify_20132014'+storeposfix, 'a')
    month13 = '2013-'+openposfix
    month14 = '2014-'+openposfix
    train1310, test1310 = get_sets(month13)
    train1410, test1410 = get_sets(month14)
    train_total = np.concatenate([train1310, train1410])
    test_total = np.concatenate([test1310, test1410])
    bestC = validate_model(train_total, output)
    svm_classifier13 = train_model(bestC, train1310, test1310, output)
    svm_classifier14 = train_model(bestC, train1410, test1410, output)
    pos13, neg13 = predict_month(month13, svm_classifier13)
    pos14, neg14 = predict_month(month14, svm_classifier14)
    output.write('----\n'+month13+' predict number: positive = ' + str(pos13) + ' negative = ' + str(neg13) + '\n')
    output.write('----\n'+month14+' predict number: positive = ' + str(pos14) + ' negative = ' + str(neg14) + '\n')
    return

# year_month: yyyy-mm
def classify_month(year_month):
    print 'this thread: ' + threading.currentThread().getName()
    output = open('classify/classify_'+year_month, 'a')
    train_total, test_total = get_sets(year_month)
    #cross validate model, get best C    
    bestC = validate_model(train_total, output)
    #train model get accuracy and parameters, get the classifier
    svm_classifier = train_model(bestC, train_total, test_total,output)
    #predict
    positive, negative = predict_month(year_month, svm_classifier)
    output.write('----\npredict number: positive = ' + str(positive) + ' negative = ' + str(negative) + '\n')
    return

def get_sets(year_month):
    satispath = '/home/ec2-user/UMMDP14/python_scripts/satis/'
    unsatispath = '/home/ec2-user/UMMDP14/python_scripts/unsatis/'
    satisfile = open(satispath + 'satis_' + year_month, 'rU')
    unsatisfile =  open(unsatispath + 'unsatis_' + year_month, 'rU')
    satistrain, satistest = get_featureset(satisfile, True)
    unsatistrain, unsatistest = get_featureset(unsatisfile, False)
    satisfile.close()
    unsatisfile.close()
    train_total = np.array(satistrain + unsatistrain)
    test_total = np.array(satistest + unsatistest)
    
    return train_total, test_total

def validate_model(train_total, output):
    #k-fold: using 3-fold
    k = 3
    kf = cross_validation.KFold(len(train_total), shuffle=True, n_folds=k) 
   
    output.write('----validate models----\n') 
    Cs = [0.000001, 0.000005, 0.00001, 0.00005, 0.0001,0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100]
    #Cs = [0.01] #test
    accuracies = []
    for theC in Cs:
        accuracy = 0
        for train_index, test_index in kf:
            kfold_train, kfold_test = train_total[train_index], train_total[test_index]
            classifier = LinearSVC(C=theC, verbose=0, dual=False, class_weight='auto')
            svm_classifier = SklearnClassifier(classifier).train(kfold_train)
            output.write('using C=: ' + str(theC)+ ' parameters: ' + np.array_str(classifier.coef_) + ' intercept: ' + np.array_str(classifier.intercept_) + '\n')
            accuracy += nltk.classify.accuracy(svm_classifier, kfold_test)
        accuracy /= k
        output.write("using C=: " + str(theC) + ' average accuracy: {0:.2f}%'.format(100*accuracy) + '\n')
        accuracies.append(accuracy)

    bestC = Cs[accuracies.index(max(accuracies))]
    return bestC 

def train_model(bestC, train_total, test_total, output):
    classifier = LinearSVC(C=bestC, verbose=0, dual=False, class_weight='auto')
    svm_classifier = SklearnClassifier(classifier).train(train_total)
    accuracy = nltk.classify.accuracy(svm_classifier, test_total)
    output.write("----training----\nusing best C= "+ str(bestC) + ' accuracy: {0:.2f}%'.format(100*accuracy) + '\n')
    output.write('parameters: ' + np.array_str(classifier.coef_) + ' intercept: ' + np.array_str(classifier.intercept_)+'\n')
    return svm_classifier

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
        featuredict = OrderedDict()
        feature_val = feature[2:-1]
        if (len(feature_val) != len(feature_key)):
            print 'error @ '
            continue

        for x in range(0,len(feature_key)):
            featuredict[feature_key[x]] = float(feature_val[x])
        del featuredict[feature_key[5]]  #delete the rs_ratio one
            
        if i in sampleindicesdict:
            trainset.append((featuredict, 1 if isSatis else -1))
        else:
            testset.append((featuredict, 1 if isSatis else -1))
    
    return trainset, testset

def predict_month(year_month, svm_classifier):
    filelist = glob.glob('../app_server_parsed/' + year_month + '*')
    positive = 0
    negative = 0
    for files in filelist:
        theFile = open(files, 'rU')
        firstLine = True
        all_sessions_per_day = []
        for line in theFile:
            if firstLine:
                firstLine = False
                continue
            feature = line.split(',')
            feature_val = feature[2:-1]
            featuredict = OrderedDict()
            if (len(feature_val) != len(feature_key)):
                print 'error @ '
                continue
            for x in range(0,len(feature_key)):
                featuredict[feature_key[x]] = float(feature_val[x])
            del featuredict[feature_key[5]]  #delete the rs_ratio one
            all_sessions_per_day.append(featuredict)
 
        predict_val = svm_classifier.classify_many(all_sessions_per_day)
        for label in predict_val:
            if label == 1:
                positive += 1
            else:
                negative += 1
        del all_sessions_per_day[:]
        del predict_val[:]
        theFile.close()

    return positive, negative 

#classify_month('2014-10')
train2years(sys.argv[1],sys.argv[2])
