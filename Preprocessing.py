from PIL import Image
from PIL.ImageOps import invert
import numpy as np
from torch.tensor import Tensor


def invert_image_path(path):
    image_file = Image.open(path)  # open colour image
    image_file = image_file.convert('L').resize([220, 155])
    image_file = invert(image_file)
    image_array = np.array(image_file)
    image_array[image_array>=50]=255
    image_array[image_array<50]=0
    return image_array


def convert_to_image_tensor(image_array):
    image_array = image_array / 255.0
    return Tensor(image_array).view(1, 220, 155)


def show_inverted(path):
    img = Image.fromarray(invert_image_path(path))
    img.show()


def invert_image(image_file):
    image_file = image_file.convert('L').resize([220, 155])
    image_file = invert(image_file)
    image_array = np.array(image_file)
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            if image_array[i][j] <= 50:
                image_array[i][j] = 0
            else:
                image_array[i][j] = 255
    return image_array



