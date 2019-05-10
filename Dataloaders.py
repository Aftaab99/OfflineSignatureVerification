from torch.utils.data import Dataset
from Preprocessing import invert_image_path, convert_to_image_tensor
from sklearn.model_selection import train_test_split
import pickle
from random import randrange

base_path_org = 'Datasets/cedar1/full_org/original_%d_%d.png'
base_path_forg = 'Datasets/cedar1/full_forg/forgeries_%d_%d.png'


def fix_pair(x, y):
    if x == y:
        return fix_pair(x, randrange(1, 24))
    else:
        return x, y


data = []
n_samples_of_each_class = 13500

prefix = '/home/aftaab/Datasets/'

for _ in range(n_samples_of_each_class):
    anchor_person = randrange(1, 55)
    anchor_sign = randrange(1, 24)
    pos_sign = randrange(1, 24)
    anchor_sign, pos_sign = fix_pair(anchor_sign, pos_sign)
    neg_sign = randrange(1, 24)
    positive = [base_path_org % (anchor_person, anchor_sign), base_path_org % (anchor_person, pos_sign), 1]
    negative = [base_path_org % (anchor_person, anchor_sign), base_path_forg % (anchor_person, neg_sign), 0]
    data.append(positive)
    data.append(negative)

train, test = train_test_split(data, test_size=0.15)
with open('train_index.pkl', 'wb') as train_index_file:
    pickle.dump(train, train_index_file)

with open('test_index.pkl', 'wb') as test_index_file:
    pickle.dump(test, test_index_file)


class TrainDataset(Dataset):

    def __init__(self):
        with open('train_index.pkl', 'rb') as train_index_file:
            self.pairs = pickle.load(train_index_file)

    def __getitem__(self, index):
        item = self.pairs[index]
        X = convert_to_image_tensor(invert_image_path(item[0]))
        Y = convert_to_image_tensor(invert_image_path(item[1]))
        return [X, Y, item[2]]

    def __len__(self):
        return len(self.pairs)


class TestDataset(Dataset):

    def __init__(self):
        with open('test_index.pkl', 'rb') as test_index_file:
            self.pairs = pickle.load(test_index_file)

    def __getitem__(self, index):
        item = self.pairs[index]
        X = convert_to_image_tensor(invert_image_path(item[0]))
        Y = convert_to_image_tensor(invert_image_path(item[1]))
        return [X, Y, item[2]]

    def __len__(self):
        return len(self.pairs)
