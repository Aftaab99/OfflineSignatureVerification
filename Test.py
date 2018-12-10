from Model import SiameseConvNet, distance_metric
from torch import load
import torch
import numpy as np
from Dataloaders import TestDataset
from torch.utils.data import DataLoader

device = torch.device('cpu')
model = SiameseConvNet()
model.load_state_dict(load(open('Models/model_epoch_2', 'rb'), map_location=device))


def compute_accuracy_roc(predictions, labels):
	dmax = np.max(predictions)
	dmin = np.min(predictions)
	nsame = np.sum(labels == 1)
	ndiff = np.sum(labels == 0)
	step = 0.001
	max_acc = 0

	d_optimal = 0
	for d in np.arange(dmin, dmax + step, step):
		idx1 = predictions.ravel() <= d
		idx2 = predictions.ravel() > d

		tpr = float(np.sum(labels[idx1] == 1)) / nsame
		tnr = float(np.sum(labels[idx2] == 0)) / ndiff

		acc = 0.5 * (tpr + tnr)

		if acc > max_acc:
			max_acc = acc
			d_optimal = d

	return max_acc, d_optimal


batch_avg_acc = 0
batch_avg_d = 0
n_batch = 0


def test(dataset_type):
	model.eval()
	global batch_avg_acc, batch_avg_d, n_batch
	loader = None
	if dataset_type == 'CEDAR1':
		test_dataset = TestDataset()
		loader = DataLoader(test_dataset, batch_size=16, shuffle=True)
	

	for batch_index, data in enumerate(loader):
		A = data[0]
		B = data[1]
		labels = data[2].long()

		f_A, f_B = model.forward(A, B)
		dist = distance_metric(f_A, f_B)

		acc, d = compute_accuracy_roc(dist.detach().numpy(), labels.detach().numpy())
		print('Max accuracy for batch {} = {} at d = {}'.format(batch_index, acc, d))
		batch_avg_acc += acc
		batch_avg_d += d
		n_batch += 1


print('CEDAR1:')
test('CEDAR1')
print('Avg acc across all batches={} at d={}'.format(batch_avg_acc / n_batch, batch_avg_d / n_batch))

batch_avg_acc = 0
n_batch = 0
batch_avg_d = 0

print('Sample dataset provided')
test('Sample')
print('Avg acc across all batches={} at d={}'.format(batch_avg_acc / n_batch, batch_avg_d / n_batch))
