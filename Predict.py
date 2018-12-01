from Preprocessing import convert_to_image_tensor, invert_image_path
from Model import SiameseConvNet
import torch
from Model import distance_metric

A = convert_to_image_tensor(invert_image_path('Images/original_1_1.png')).view(1, 1, 220, 155)
P = convert_to_image_tensor(invert_image_path('Images/original_1_2.png')).view(1, 1, 220, 155)
N = convert_to_image_tensor(invert_image_path('Images/forgeries_1_1.png')).view(1, 1, 220, 155)
print(A.sum(1).sum().detach().numpy())
print(P.sum(1).sum().detach().numpy())
print(N.sum(1).sum().detach().numpy())

device = torch.device('cpu')
model = SiameseConvNet().eval()

model.load_state_dict(torch.load('Models/model_epoch_2', map_location=device))

f_A, f_P = model.forward(A, P)
dist_AP = distance_metric(f_A, f_P).detach().numpy()
print(dist_AP)
pred = "tbd"
if dist_AP <= 0.1618:
	pred = "Same"
else:
	pred = "Diff"
print('Prediction 1:{}'.format(pred))
