import requests
import os
import zipfile


def download_file_from_google_drive(id, destination):
	URL = "https://drive.google.com/uc?export=download"

	session = requests.Session()

	response = session.get(URL, params={'id': id}, stream=True)
	token = get_confirm_token(response)

	if token:
		params = {'id': id, 'confirm': token}
		response = session.get(URL, params=params, stream=True)

	save_response_content(response, destination)


def get_confirm_token(response):
	for key, value in response.cookies.items():
		if key.startswith('download_warning'):
			return value

	return None


def save_response_content(response, destination):
	CHUNK_SIZE = 32768

	with open(destination, "wb") as f:
		for chunk in response.iter_content(CHUNK_SIZE):
			if chunk:  # filter out keep-alive new chunks
				f.write(chunk)


def extract(file_path):
	zip_ref = zipfile.ZipFile(file_path, 'r')
	zip_ref.extractall(os.path.dirname(file_path))
	zip_ref.close()


if __name__ == "__main__":
	model_file_id = '1jR1CIgSuBy9_CV4zkSyojetCtU7Drxn2'
	model_destination = 'Models/model_epoch_2'
	dataset_file_id = '1w2DEYX2pBhBNS2l4sqrl8j-Am4cNSBoZ'
	dataset_destination = 'Datasets/cedar1.zip'

	if not os.path.exists('./Datasets/cedar1/'):
		os.mkdir('./Datasets')
		print('Downloading dataset...')
		download_file_from_google_drive(dataset_file_id, dataset_destination)
		print('Extracting data...')
		extract('./Datasets/cedar1.zip')
		os.remove('./Datasets/cedar1.zip')

	if not os.path.exists('./Models/model_epoch_2'):
		os.mkdir('./Models')
		print('Downloading pretrained-model...')
		download_file_from_google_drive(model_file_id, model_destination)


