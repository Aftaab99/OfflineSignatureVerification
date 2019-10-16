## Offline Writer Independent signature verification

### Setting up locally

Download the dependencies(for conda users)

	conda env create -f projenv.yml
	
They can be installed using pip via
    
    pip install -r requirements.txt
    
Then download the pretrained model and dataset

    python DownloadData.py
    
After setting the environment and downloading the pretrained model, start the web server using

	python main.py

### Models used
Used a Convolutional Siamese network along with the Constrastive loss function. I chose Euclidian distance as the distance metric for comparing the output feature vectors.

### Accuracy
The model acheived an accuracy of 78.34% on the CEDAR signature dataset(test set size was around 4100 samples). 
Deviations of 1-2% are possible as accuracy depends on the threshold.
The threshold for the siamese network was computed by taking the average of True positive rate and True negative rate using ROC.

### Preprocessing
Images were converted to grayscale, inverted and scaled down to 0 or up to 255 depending on whether the pixel value was below or above 50.
Image tensor sizes of 225x155 were fed into the model.
Images were grouped in pairs of genuine and forged images, where the label was 1 if both were genuine and of the same writer and 0 otherwise.
13500 image pairs of each label where chosen, 15% of which were used for testing.

##### Original image
![Original image](https://github.com/Aftaab99/OfflineSignatureVerification/blob/master/images/original_sign.png)

##### Preprocessed image
![Preprocessed image](https://github.com/Aftaab99/OfflineSignatureVerification/blob/master/images/preprocessed_sign.png)


### Dataset
The CEDAR signature dataset is one of the benchmark datasets for signature verification. It consists of 24 genuine and forged signatures each from 55 different signers.

[Dataset link](http://www.cedar.buffalo.edu/NIJ/data/signatures.rar)


### References
1. [SigNet: Convolutional Siamese Network for Writer Independent Offline SignatureVerification](https://arxiv.org/pdf/1707.02131.pdf)
