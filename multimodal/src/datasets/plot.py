import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class Plot:
  def __init__(self):
    pass

  def plot(self, image_path, image_title = ""):
    img = Image.open(image_path)
    img_array = np.array(img)

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(img_array)

    ax.set_title(image_title)
    ax.axis('off')

    plt.show()
