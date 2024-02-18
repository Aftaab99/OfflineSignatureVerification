import os
import zipfile
import gdown


def extract(file_path):
    zip_ref = zipfile.ZipFile(file_path, 'r')
    zip_ref.extractall(os.path.dirname(file_path))
    zip_ref.close()


if __name__ == "__main__":
    model_file_id = '1Dt-np-v30w0X1OSqqcKpzvifktq4k7r-'
    model_destination = 'Models/model_large_epoch_20'
    dataset_file_id = '1w2DEYX2pBhBNS2l4sqrl8j-Am4cNSBoZ'
    dataset_destination = 'Datasets/cedar1.zip'

    if not os.path.exists('./Datasets/cedar1/'):
        os.mkdir('./Datasets')
        print('Downloading dataset...')
        gdown.download('https://drive.google.com/uc?id={}'.format(dataset_file_id), dataset_destination, verify=False)
        print('Extracting data...')
        extract(dataset_destination)
        os.remove(dataset_destination)

    if not os.path.exists('./Models/model_large_epoch_20'):
        os.mkdir('./Models')
        print('Downloading pretrained-model...')
        gdown.download('https://drive.google.com/uc?id={}'.format(model_file_id), model_destination, verify=False)
