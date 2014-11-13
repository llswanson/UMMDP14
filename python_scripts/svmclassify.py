import os
import pdb
import random
from collections import OrderedDict

import numpy as np
import nltk
from sklearn import cross_validation
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

feature_key = ['search','retrieval','retrieval_from_search','preview','preview_from_search','rs_ratio','add_to_my_list','email','print','export_easylib']

# year_month: yyyy-mm
def main(year_month):
    satispath = '/home/ec2-user/UMMDP14/python_scripts/satis/'
    unsatispath = '/home/ec2-user/UMMDP14/python_scripts/unsatis/'
    satisfile = open(satispath + 'satis_' + year_month, 'rU')
    unsatisfile =  open(unsatispath + 'unsatis_' + year_month, 'rU')
    satistrain, satistest = get_featureset(satisfile, True)
    unsatistrain, unsatistest = get_featureset(unsatisfile, False)
    satisfile.close()
    unsatisfile.close()
    #train
    train_total = np.array(satistrain + unsatistrain)
    test_total = np.array(satistest + unsatistest)
    #k-fold: using 3-fold
    k = 3
    kf = cross_validation.KFold(len(train_total), shuffle=True, n_folds=k) 
    '''
    Cs = [0.000001, 0.000005, 0.00001, 0.00005, 0.0001,0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100]
    accuracies = []
    for theC in Cs:
        accuracy = 0
        for train_index, test_index in kf:
            kfold_train, kfold_test = train_total[train_index], train_total[test_index]
            classifier = LinearSVC(C=theC, verbose=0, dual=False, class_weight='auto')
            svm_classifier = SklearnClassifier(classifier).train(kfold_train)
            print 'using C=: ' + str(theC)+ ' parameters: ' + np.array_str(classifier.coef_) + ' intercept: ' + np.array_str(classifier.intercept_)
            accuracy += nltk.classify.accuracy(svm_classifier, kfold_test)
        accuracy /= k
        print "using C=: " + str(theC) + ' average accuracy: {0:.2f}%'.format(100*accuracy)
        accuracies.append(accuracy)

    finalC = Cs[accuracies.index(max(accuracies))]
    '''
    classifier = LinearSVC(C=0.01, verbose=0, dual=False, class_weight='auto')
    svm_classifier = SklearnClassifier(classifier).train(train_total)
    accuracy = nltk.classify.accuracy(svm_classifier, test_total)
    #print "final using C= "+ str(finalC) + ' accuracy: {0:.2f}%'.format(100*accuracy)
    print 'parameters: ' + np.array_str(classifier.coef_) + ' intercept: ' + np.array_str(classifier.intercept_)
    pdb.set_trace()

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
        featuredict = OrderedDict()
        feature_val = feature[2:-1]
        if (len(feature_val) != len(feature_key)):
            print 'error @ '
            continue

        for x in range(0,len(feature_key)):
            featuredict[feature_key[x]] = float(feature_val[x])
            
        if i in sampleindicesdict:
            trainset.append((featuredict, 1 if isSatis else -1))
        else:
            testset.append((featuredict, 1 if isSatis else -1))
    
    return trainset, testset

main('2014-10')
