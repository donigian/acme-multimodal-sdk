import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

class Plot:
  def __init__(self, image_path):
    self.image_path = image_path
  
  def plot(self):
    image = plt.imread(self.image_path)
    plt.imshow(image)
    plt.show()


Plot.plot('images/imageid_55ca238de12d4b65a650207f050db124.jpeg')