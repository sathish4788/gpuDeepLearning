__author__ = 'caturner3'

import sys
import cPickle as pickle
import numpy as np
from sklearn.preprocessing import Imputer, OneHotEncoder
import re


def pickle_data():
    """
    This single-function file is for pickling datasets to be sent to each algorithm
    """
    if(len(sys.argv) <= 1):
        print >> sys.stderr, "Proper usage of pickle_data.py: pickle_data.py <dataset>"
        sys.exit(1)
    dataset = sys.argv[1]
    if dataset == "diabetes":
        # The goal is to predict readmission
        print "Using "+dataset+" dataset"
        datafile = open("../data/dataset_diabetes/diabetic_data.csv")
        datalines = datafile.readlines()
        datafile.close()
        datalines = datalines[1:] # remove the headers
        for i in range(len(datalines)):
            # The first 2 columns are unique identifiers - we know each row is a patient
            datalines[i] = datalines[i].strip().split(",")[2:]

        temp_data_mat = np.matrix(datalines)
        # We need to convert categorical data to ints/floats so we can use one hot encoding
        data_mat = []
        for col in temp_data_mat.T:
            unique_vals = []
            col_list = col.tolist()
            for ii in range(len(col_list)):
                for i in range(len(col_list[ii])):
                    item = col_list[ii][i]
                    if item not in unique_vals:
                        unique_vals.append(item)
                    if item != "?" and not re.match("^\d+",item):
                        col_list[ii][i] = unique_vals.index(item)
                    elif item == "?":
                        col_list[ii][i] = "NaN"
            data_mat.append(col_list[0])

        # convert out of the column format
        data_mat = np.array(data_mat).T
        # Imputer converts missing values (?'s) to the mean of the column
        #   mean, median, and mode are available options for strategy
        imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
        print data_mat[0]
        data_mat = imp.fit_transform(data_mat)
        print data_mat[0]
        #imp.fit(data_mat)
        #print data_mat[0]
        #imp.transform(data_mat)
        #print data_mat[0]

        encoder = OneHotEncoder()
        #data_mat = encoder.fit(data_mat)
        encoder.fit(data_mat)
        y = data_mat[:,-1]
        x = data_mat[:,:-1]
        print "y:", y
        print "x:", x

    elif dataset == "heritage":
        print "Using "+dataset+" dataset"
    elif dataset == "pubmed":
        print "Using "+dataset+" dataset"
    else:
        print "Improper dataset specified"
        sys.exit(1)

pickle_data()