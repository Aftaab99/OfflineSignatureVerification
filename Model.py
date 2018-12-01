from torch.nn import Linear, Conv2d, MaxPool2d, LocalResponseNorm, Dropout
from torch.nn.functional import relu
from torch.nn import Module
import torch.nn.functional as F
import torch


class SiameseConvNet(Module):
	def __init__(self):
		super().__init__()
		self.conv1 = Conv2d(1, 5, kernel_size=(11, 11), stride=1)
		self.lrn1 = LocalResponseNorm(5, alpha=1e-4, beta=0.75, k=2)
		self.pool1 = MaxPool2d(kernel_size=(3, 3), stride=2)
		self.conv2 = Conv2d(5, 12, kernel_size=(5, 5), stride=1, padding=2)
		self.lrn2 = LocalResponseNorm(5, alpha=1e-4, beta=0.75, k=2)
		self.pool2 = MaxPool2d(kernel_size=(3, 3), stride=2)
		self.dropout1 = Dropout(0.3)
		self.conv3 = Conv2d(12, 16, kernel_size=(3, 3), stride=1, padding=1)
		self.fc1 = Linear(51 * 35 * 16, 1024, bias=False)
		self.dropout2 = Dropout(0.4)
		self.fc2 = Linear(1024, 128, bias=False)

	def forward_once(self, x):
		x = relu(self.conv1(x))
		x = self.lrn1(x)
		x = self.pool1(x)
		x = relu(self.conv2(x))
		x = self.lrn2(x)
		x = self.pool2(x)
		x = self.dropout1(x)
		x = relu(self.conv3(x))
		x = x.view(-1, 51 * 35 * 16)
		x = relu(self.fc1(x))
		x = self.dropout2(x)
		x = relu(self.fc2(x))
		return x

	def forward(self, x, y):
		f_x = self.forward_once(x)
		f_y = self.forward_once(y)
		return f_x, f_y


def distance_metric(features_A, features_B):
	batch_losses = F.pairwise_distance(features_A, features_B)
	return batch_losses


class ContrastiveLoss(torch.nn.Module):

	def __init__(self, margin=2):
		super(ContrastiveLoss, self).__init__()
		self.margin = margin

	def forward(self, output1, output2, label):
		euclidean_distance = F.pairwise_distance(output1, output2)
		loss_contrastive = torch.mean((1 - label) * torch.pow(euclidean_distance, 2) +
									  (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))

		return loss_contrastive
