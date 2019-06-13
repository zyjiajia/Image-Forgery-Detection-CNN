from cnn.cnn_implement import SimpleCNN
from src.feature_fusion.feature_fusion import get_Yi, get_Y_hat, get_dummy_Yi
import torch
import numpy as np


def create_SVM_features(model):

    # for every image (RAFAIL)

        # get name and label (RAFAIL)

        # generate pathes (RAFAIL)

        Y = []  # init Y (KYRIAKOS)

        # for every patch (RAFAIL)

            #Yi = get_Yi(model=model, patch=patch)  # call CNN -> Yi (KYRIAKOS)

        for _ in range(3):

            Yi = get_dummy_Yi()
            Y.append(Yi)  # append Yi to Y (KYRIAKOS)

        Y = np.vstack(tuple(Y))

        print(Y)

        print(Y.shape)

        Y_hat = get_Y_hat(y=Y, operation="mean")  # create Y_hat with mean or max (KYRIAKOS)

        # save the feature vector to csv (KYRIAKOS)

        print(Y_hat)

        #csv type [im_name][label][f1,f2,...,fK]

        return None


def main():
    model = SimpleCNN()
    model.load_state_dict(torch.load('Simple_Cnn.pt'))
    model.eval()


create_SVM_features(None)