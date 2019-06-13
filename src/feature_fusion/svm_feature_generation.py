from cnn.cnn_implement import SimpleCNN
from src.feature_fusion.feature_fusion import get_Yi, get_Y_hat, get_dummy_Yi
import torch
import numpy as np
import pandas as pd
import time
from src.feature_fusion.feature_extraction import get_images_and_labels, get_patches


def create_SVM_features(model):
    # for every image (RAFAIL)
    #
    # for image_name in images.keys():
    #     # get name and label (RAFAIL)
    #     image = images[image_name]['mat']
    #     label = images[image_name]['label']
    #
    #     # generate patches (RAFAIL)
    #     patches = get_patches(image, stride=128)
    #
        # for every patch (RAFAIL)
        # for patch in patches:
        #     pass

        #Yi = get_Yi(model=model, patch=patch)  # call CNN -> Yi (KYRIAKOS)

    df = pd.DataFrame()
    images = get_images_and_labels()

    for image_name in images.keys():  # images

        image = images[image_name]['mat']
        label = images[image_name]['label']
        Y = []  # init Y (KYRIAKOS)

        patches = get_patches(image, stride=128)

        for patch in patches:
            Yi = get_dummy_Yi()  # call CNN -> Yi with the patch (KYRIAKOS)
            Y.append(Yi)  # append Yi to Y (KYRIAKOS)

        Y = np.vstack(tuple(Y))

        print(Y)

        print(Y.shape)

        Y_hat = get_Y_hat(y=Y, operation="mean")  # create Y_hat with mean or max (KYRIAKOS)

        print(Y_hat)

        df = pd.concat([df, pd.DataFrame(Y_hat)], axis=1, sort=False)

    # save the feature vector to csv (KYRIAKOS)
    final_df = df.T
    final_df.columns = get_df_column_names()
    final_df.to_csv('test.csv', index=False)  # csv type [im_name][label][f1,f2,...,fK]


def get_df_column_names():
    names = []
    for i in range(400):
        names.append("f"+str(i+1))
    return names


def main():
    model = SimpleCNN()
    model.load_state_dict(torch.load('Simple_Cnn.pt'))
    model.eval()


if __name__ == '__main__':
    create_SVM_features(None)

