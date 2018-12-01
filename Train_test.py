from Dataloaders import TrainDataset, TestDataset
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
test_dataset = TestDataset()
test_loader = DataLoader(test_dataset, batch_size=32)


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


def compute_accuracy_roc(predictions, labels):
	dmax = np.max(predictions)
	dmin = np.min(predictions)
	nsame = np.sum(labels == 1)
	ndiff = np.sum(labels == 0)

	step = 0.01
	max_acc = 0
	d_optimal = 0
	for d in np.arange(dmin, dmax + step, step):
		idx1 = predictions.ravel() <= d
		idx2 = predictions.ravel() > d

		tpr = float(np.sum(labels[idx1] == 1)) / nsame
		tnr = float(np.sum(labels[idx2] == 0)) / ndiff
		acc = 0.5 * (tpr + tnr)
		print('ROC: Acc={}, TP={}, TN = {}'.format(acc, tpr, tnr))

		if (acc > max_acc):
			max_acc = acc
			d_optimal = d

	return max_acc, d_optimal


def test():
	model.eval()
	for batch_index, data in enumerate(test_loader):
		A = data[0]
		B = data[1]
		labels = data[2].long()

		f_A, f_B = model.forward(A, B)
		dist = distance_metric(f_A, f_B)
		acc, d = compute_accuracy_roc(dist.detach().numpy(), labels.detach().numpy())
		print('Max accuracy for batch {} = {} at d={}'.format(batch_index, acc, d))


test()
