import random
from random import shuffle
import os

cwd=os.getcwd()

def load5foldData(obj):
    if obj == "Guba":
        labelPath = os.path.join(cwd,"data/Guba/Guba_post_label.txt")
        print("loading Guba label:")
        B, S = [], []
        l1 = l2 = 0
        labelDic = {}
        for line in open(labelPath):
            line = line.rstrip()
            eid,label = line.split('\t')[0], line.split('\t')[1]
            labelDic[eid] = int(label)
            if labelDic[eid]==1:
                B.append(eid)
                l1 += 1
            if labelDic[eid]==0:
                S.append(eid)
                l2 += 1
        print(len(labelDic))
        print(l1, l2)
        random.shuffle(B)
        random.shuffle(S)
        # B is F and S is T

        fold0_x_test, fold1_x_test, fold2_x_test, fold3_x_test, fold4_x_test = [], [], [], [], []
        fold0_x_train, fold1_x_train, fold2_x_train, fold3_x_train, fold4_x_train = [], [], [], [], []
        leng1 = int(l1 * 0.2)
        leng2 = int(l2 * 0.2)
        fold0_x_test.extend(B[0:leng1])
        fold0_x_test.extend(S[0:leng2])
        fold0_x_train.extend(B[leng1:])
        fold0_x_train.extend(S[leng2:])
        fold1_x_train.extend(B[0:leng1])
        fold1_x_train.extend(B[leng1 * 2:])
        fold1_x_train.extend(S[0:leng2])
        fold1_x_train.extend(S[leng2 * 2:])
        fold1_x_test.extend(B[leng1:leng1 * 2])
        fold1_x_test.extend(S[leng2:leng2 * 2])
        fold2_x_train.extend(B[0:leng1 * 2])
        fold2_x_train.extend(B[leng1 * 3:])
        fold2_x_train.extend(S[0:leng2 * 2])
        fold2_x_train.extend(S[leng2 * 3:])
        fold2_x_test.extend(B[leng1 * 2:leng1 * 3])
        fold2_x_test.extend(S[leng2 * 2:leng2 * 3])
        fold3_x_train.extend(B[0:leng1 * 3])
        fold3_x_train.extend(B[leng1 * 4:])
        fold3_x_train.extend(S[0:leng2 * 3])
        fold3_x_train.extend(S[leng2 * 4:])
        fold3_x_test.extend(B[leng1 * 3:leng1 * 4])
        fold3_x_test.extend(S[leng2 * 3:leng2 * 4])
        fold4_x_train.extend(B[0:leng1 * 4])
        fold4_x_train.extend(B[leng1 * 5:])
        fold4_x_train.extend(S[0:leng2 * 4])
        fold4_x_train.extend(S[leng2 * 5:])
        fold4_x_test.extend(B[leng1 * 4:leng1 * 5])
        fold4_x_test.extend(S[leng2 * 4:leng2 * 5])

    fold0_test = list(fold0_x_test)
    shuffle(fold0_test)
    fold0_train = list(fold0_x_train)
    shuffle(fold0_train)
    fold1_test = list(fold1_x_test)
    shuffle(fold1_test)
    fold1_train = list(fold1_x_train)
    shuffle(fold1_train)
    fold2_test = list(fold2_x_test)
    shuffle(fold2_test)
    fold2_train = list(fold2_x_train)
    shuffle(fold2_train)
    fold3_test = list(fold3_x_test)
    shuffle(fold3_test)
    fold3_train = list(fold3_x_train)
    shuffle(fold3_train)
    fold4_test = list(fold4_x_test)
    shuffle(fold4_test)
    fold4_train = list(fold4_x_train)
    shuffle(fold4_train)

    return list(fold0_test),list(fold0_train),\
           list(fold1_test),list(fold1_train),\
           list(fold2_test),list(fold2_train),\
           list(fold3_test),list(fold3_train),\
           list(fold4_test), list(fold4_train)
