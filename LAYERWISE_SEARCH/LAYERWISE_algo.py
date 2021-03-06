import numpy as np
import random
import sys
sys.path.insert(0,'/homes/nj2217/FINAL_PROJECT/MAIN')
# sys.path.insert(0,'/d/PROJECT/FINAL_PROJECT/MAIN')

from HELPER_FUNCTION import *
from TRAIN_MODEL_CIFAR10 import *
from TRAIN_MODEL_MNIST import *

MAX_ACTION = 16
MAX_STATE = 4
LAYER_ACTION = ['c_1','c_2','c_3','c_4','c_5','c_6','c_7','c_8','c_9','c_10','c_11',\
                'c_12','m_1','m_2','m_3','s']

MAX_INDEX_MODEL_ARRAY = 1 + MAX_STATE + 2
INDEX_MODEL = 0
INDEX_ACCURACY = -2

def create_empty_array():
    ###########################################################################
    # FUNCTION DESCRIPTION: create empty array equal to state total state space
    #                       with each row consists of model_name,topologies,
    #                       accuracy and loss with '-'
    ###########################################################################

    final_array = []
    for _ in range(MAX_ACTION*MAX_STATE):
        temp_array = ['-']*MAX_INDEX_MODEL_ARRAY
        final_array.append(temp_array)
    return final_array


def init_layer_action(final_array,index_hill_level):
    ###########################################################################
    # FUNCTION DESCRIPTION: initialize array with each possible action
    ###########################################################################

    for index in range(MAX_ACTION):
        final_array[index+index_hill_level*MAX_ACTION][index_hill_level+1] = LAYER_ACTION[index]
    return final_array

def use_best_layer(final_array,best_layer,index_hill_level):
    ###########################################################################
    # FUNCTION DESCRIPTION: assign the layer with highest accuracy for next training
    ###########################################################################

    start_index = (1+index_hill_level)*MAX_ACTION
    final_index = MAX_STATE*MAX_ACTION
    for index in range(start_index,final_index):
        final_array[index][index_hill_level+1] = best_layer
    return final_array

def layerwise_search(DATASET,SAVE_FILE):
    ###########################################################################
    # FUNCTION DESCRIPTION: do layerwise search algorithm to find the topology that gives
    #                       highest validation accuracy
    ###########################################################################

    model_num = 0
    final_array = create_empty_array()

    for index_hill_level in range(MAX_STATE):
        final_array = init_layer_action(final_array,index_hill_level)
        accuracy_array = []

        for index_layer_in_hill in range(MAX_ACTION):

            for index_model_array in range(MAX_INDEX_MODEL_ARRAY):
                current_model_array = final_array[index_layer_in_hill+index_hill_level*MAX_ACTION]
                current_model_array[INDEX_MODEL] = 'model_'+str(model_num)

            if DATASET == 'cifar10':
                # accuracy = random.uniform(0, 1)
                accuracy = train_model_cifar10(current_model_array, DATASET)
            elif DATASET == 'mnist':
                # accuracy = random.uniform(0, 1)
                accuracy = train_model_mnist(current_model_array,DATASET)

            accuracy_array.append(accuracy)
            current_model_array[INDEX_ACCURACY] =  accuracy

            eval_result = ['Unknown',accuracy]
            model_num += 1

            save_trained_model_in_csv(SAVE_FILE,current_model_array,eval_result)

        max_accuracy = max(accuracy_array)
        index_best_layer = accuracy_array.index(max_accuracy)
        best_layer = LAYER_ACTION[index_best_layer]

        if index_hill_level != MAX_STATE-1:
            final_array = use_best_layer(final_array, best_layer,index_hill_level)

    print(final_array)

def main():
    DATASET = 'cifar10'
    SAVE_FILE = 'hc_cifar10.csv'
    layerwise_search(DATASET,SAVE_FILE)

if __name__ == '__main__':
    main()
