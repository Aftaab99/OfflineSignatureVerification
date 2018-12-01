## Offline Writer Independent signature verification

### Setting up project Environment

	conda env create -f projenv.yml

After setting the environment and downloading the pretrained model, start the web server using

	python main.py

### Models used
Used a  convolutional siamese network along with the constrastive loss function. I chose euclidien distance as the distance metric for comparing the output feature vectors.
Flask was used for the web demo.
Download the [model](https://drive.google.com/open?id=1jR1CIgSuBy9_CV4zkSyojetCtU7Drxn2) and place it in the Models directory.

### Accuracy
The model acheived an accuracy of 74.34% on the CEDAR1 dataset(test set size was around 4100 samples). 
It obtained 83% accuracy on the training set provided.
Deviations of 1-2% are possible.

### Preprocessing
Images were converted to grayscale, inverted and scaled down to 0 or up to 255 depending on whether the pixel value was below or above 50(this was done to remove any background specks and proved to simple yet effective technique for this task).
Image tensor sizes of 225x155 were fed into the model.

### Dataset
[Dataset available here](https://drive.google.com/open?id=14FpvDPGy0TtRrJL8TLgaHpPzJhB2duGA).

[Original link](http://www.cedar.buffalo.edu/NIJ/data/signatures.rar)

For training or testing replace the 'prefix' variable in Dataloaders.py with the path to the dataset folder's parent directory.

### Trying the web demo
[Web demo](https://signature-verification.herokuapp.com/)
