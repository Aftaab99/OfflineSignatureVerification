from torch.utils.data import Dataset
from Preprocessing import invert_image_path, convert_to_image_tensor
from sklearn.model_selection import train_test_split
import pickle
import os
from random import randrange

from glob import glob, fnmatch

prefix = '/home/aftaab/Datasets/'
base_path_org = prefix + 'sample_Signature/genuine/NFI-{}{}{}.png'
pattern = 'NFI-{}?????.png'
base_path_forg = prefix + 'sample_Signature/forged/NFI-{}{}{}.png'
data = []
all_pos = glob(base_path_org.format('*', '*', '*'))
all_neg = glob(base_path_forg.format('*', '*', '*'))


def match_files(files, pattern):
	res = []
	for file in files:
		fname = os.path.basename(file)
		if fname[4:7] == pattern:
			res.append(file)
	return res


def generate_seq3():
	pattern = "{}{}{}"
	for x in range(0, 1):
		for y in range(0, 9):
			for z in range(0, 9):
				yield pattern.format(x, y, z)


def generate_seq2():
	pattern = "{}{}"
	for x in range(0, 1):
		for y in range(0, 9):
			yield pattern.format(x, y)


for _, person_id in enumerate(generate_seq3()):
	for _, sign_id in enumerate(generate_seq2()):
		for _, signer_id in enumerate(generate_seq3()):
			pos_matches = match_files(all_pos, person_id)
			neg_matches = match_files(all_neg, person_id)
			anchor = base_path_org.format(person_id, sign_id, signer_id)
			for pm in pos_matches:
				item = [anchor, pm, 1]
				data.append(item)
			for nm in neg_matches:
				item = [anchor, nm, 0]
				data.append(item)

files_present = []
gc = 0
fc = 0
for item in data:
	for pos in all_pos:
		if pos == item[0]:
			if item[2] == 1:
				gc += 1
			else:
				fc += 1
			files_present.append(item)
print("Genuine pairs: {}\nForged pairs: {}".format(gc, fc))


class SampleTestDataset(Dataset):
	def __init__(self):
		self.data = files_present

	def __getitem__(self, index):
		item = self.data[index]
		X = convert_to_image_tensor(invert_image_path(item[0]))
		Y = convert_to_image_tensor(invert_image_path(item[1]))
		return [X, Y, item[2]]

	def __len__(self):
		return len(self.data)
