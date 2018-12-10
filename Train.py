from Dataloaders import TrainDataset
from Model import SiameseConvNet, ContrastiveLoss, distance_metric
from torch.optim import RMSprop, Adam
from torch.utils.data import DataLoader
import numpy as np
from torch import save

model = SiameseConvNet()
criterion = ContrastiveLoss()
optimizer = Adam(model.parameters())

train_dataset = TrainDataset()
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)


def checkpoint(epoch):
	file_path = "Models/model_epoch_%d" % epoch
	with open(file_path, 'wb') as f:
		save(model.state_dict(), f)


def train(epoch):
	total_loss = 0
	for batch_index, data in enumerate(train_loader):
		A = data[0]
		B = data[1]
		optimizer.zero_grad()
		label = data[2].float()
		f_A, f_B = model.forward(A, B)
		loss = criterion(f_A, f_B, label)
		total_loss += loss.item()
		print('Epoch {}, batch {}, loss={}'.format(epoch, batch_index, loss.item()))
		loss.backward()
		optimizer.step()
	print('Average epoch loss={}'.format(total_loss / (len(train_dataset) // 16)))


for e in range(1, 21):
	train(e)
	checkpoint(e)


