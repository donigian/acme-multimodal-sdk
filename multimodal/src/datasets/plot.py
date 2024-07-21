import pathlib
import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import utils
from torchvision.io import read_image
from torchvision.utils import make_grid
from torchvision.transforms import functional as F
from typing import List
plt.rcParams["savefig.bbox"] = 'tight'

class ImagePlotter:
    """
    A class for plotting images and image grids.
    """

    def __init__(self):
        pass

    def plot_image(self, image_path: str, title: str = "") -> None:
        """
        Plots a single image from a given path.

        Args:
            image_path (str): Path to the image file.
            title (str, optional): Title for the plot. Defaults to "".
        """
        img = Image.open(image_path)
        img_array = np.array(img)

        fig, ax = plt.subplots()
        ax.imshow(img_array)

        ax.set_title(title)
        ax.axis('off')

        plt.show()

    def plot_images(self, images) -> None:
        """
        Plots a list of images in a grid format.

        Args:
            images: List of images (tensors or NumPy arrays).
        """
        if not isinstance(images, list):
            imgs = [images]
        fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
        for i, img in enumerate(imgs):
            img = img.detach()
            img = F.to_pil_image(img)
            axs[0, i].imshow(np.asarray(img))
            axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
            
    def plot_image_paths(self, image_paths: List[str]) -> None:
        """
        Plots a list of images from their paths.

        Args:
            image_paths (List[str]): List of image file paths.
        """
        images = [read_image(path) for path in image_paths]
        self.plot_images(make_grid(images))
