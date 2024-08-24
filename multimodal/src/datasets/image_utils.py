import os
import pandas as pd
from PIL import Image
from typing import List, Set
from collections import namedtuple

from datasets import load_dataset
from cleanvision import Imagelab

class ImageUtils:
  """
  A class for finding issues with images.
  """

  def __init__(self, image_dir : str):
    self.image_dir = image_dir
    self.image_examiner = None
    self.file_to_issue_map = {}
    self.all_images = []
    self.formatted_dataset = None
    self.formatted_train_dataset = None
    self.formatted_test_dataset = None
    self.images_no_issues = None
    self.labels = []
    self.issue_types = {"dark": {}, "blurry": {}, "exact_duplicates": {},
              "near_duplicates": {"hash_type": "phash"}, "low_information": {}, "light": {},
              "grayscale": {}, "odd_aspect_ratio": {}}  

  def find_images_in_directory(self) -> List[str]:
    """
    Finds images in a directory.

    Returns:
      A list of image filenames.
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for filename in os.listdir(self.image_dir):
      if any(filename.lower().endswith(ext) for ext in image_extensions):
        self.all_images.append(filename)
    return self.all_images

  def find_issues_in_images(self) -> None:
    """
    Finds different types of issues commonly found in images.
    """
    self.image_examiner = Imagelab(data_path=self.image_dir)
    self.image_examiner.find_issues(issue_types=self.issue_types)

  def report_image_issue_types_found(self) -> pd.DataFrame:
    """
    Finds different types of issues commonly found in images.

    Returns:
      A dataframe of issues found in directory of images.
    """
    self.issue_types_found = self.image_examiner.issue_summary.query("num_images > 0")["issue_type"].tolist()
    return self.image_examiner.issue_summary.query("num_images > 0")

  def set_filenames_with_specific_issue(self, image_issue_type: str) -> None:
    """
    Store mapping of image and the type of issues it contains.

    Args:
      image_issue_type: Specific type of image issue.
    """
    list_of_offending_images = self.image_examiner.issues[self.image_examiner.issues[f"is_{image_issue_type}_issue"] == True].index.tolist()
    self.file_to_issue_map[image_issue_type] = list_of_offending_images

  def get_list_of_images_no_issues(self) -> List[str]:
    """
    Remove images with issues from original set of images.

    Returns:
      A list of images which don't contain any issues.
    """
    issue_types_found = self.image_examiner.issue_summary.query("num_images > 0")["issue_type"].tolist()
    print(f" issue_types_found : {issue_types_found}")
    for issue in issue_types_found:
      self.set_filenames_with_specific_issue(issue)
    formatted_set = self._remove_prefix_from_set(set(list(self.file_to_issue_map.values())[0]))
    self.images_no_issues = list( set(self.all_images) - formatted_set )
    return self.images_no_issues

  def walk_direcotry_assign_labels_by_image_paths(self):
    """
    Walks through a directory and assigns labels to images based on their paths.

    """
    pass

  def generate_labels(self, set_name: str, prompt_to_create_label: str):
    """
    Create labels for dataset.

    Returns:
      A dataset of labels.
    """
    # Define a namedtuple
    Scene = namedtuple('Scene', ['image', 'caption', 'label'])

    # Create namedtuple instances
    if set_name == 'train':
      dataset = self.formatted_train_dataset
    else:
      dataset = self.formatted_test_dataset

    for example in dataset:
      # Access elements of each example, e.g.,
      image = example['image']
      caption = example['caption']

      question = prompt_to_create_label
      prompt = f"Question: {question} Answer:" 

      inputs = processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)

      generated_ids = model.generate(**inputs, max_new_tokens=10)
      contains_human_or_not = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
      self.labels.append(Scene(image, caption, contains_human_or_not))

  def create_formatted_dataset(self, train_test_ration=0.20):
    """
    Create an Arrow formatted dataset.

    Returns:
      None.
    """
    self.formatted_dataset = load_dataset("imagefolder", data_dir=self.image_dir)
    train_test_split = self.formatted_dataset["train"].train_test_split(test_size=train_test_ration)
    self.formatted_train_dataset = train_test_split["train"]
    self.formatted_test_dataset = train_test_split["test"]


  def _remove_prefix_from_set(self, original_set, prefix="/content/images/") -> Set:
    """Removes the given prefix from each string in the set.

    Args:
      original_set: The set of strings.
      prefix: The prefix to remove.

    Returns:
      A new set with the prefix removed from each string.
    """
    return {s[len(prefix):] if s.startswith(prefix) else s for s in original_set}
