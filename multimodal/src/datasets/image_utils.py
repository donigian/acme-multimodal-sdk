from cleanvision import Imagelab
from typing import List
import os
import pandas as pd

class ImageUtils:
  """
  A class for finding issues with images.
  """

  def __init__(self, image_dir : str):
    self.image_dir = image_dir
    self.image_examiner = None
    self.file_to_issue_map = {}
    self.all_images = []
    self.images_no_issues = None
    self.issue_types = {"dark": {}, "blurry": {}, "exact_duplicates": {},
              "near_duplicates": {"hash_type": "phash"}, "low_information": {}, "light": {},
              "grayscale": {}, "odd_aspect_ratio": {}}  

  def find_images_in_directory(self):
    """
    Finds images in a directory.

    Args:
      image_dir: The directory containing the images.

    Returns:
      A list of images.
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

  def visualize_images_with_issues():
    """
    Produce a report with issues found in images
    """
    return self.image_examiner.report(issue_types=self.issue_types)

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
    Finds images which contain specific type of issue.

    Args:
      image_issue_type: Specific type of image issue.

    Returns:
      A list of filenames of images which contain offending issue.
    """
    list_of_offending_images = self.image_examiner.issues[self.image_examiner.issues[f"is_{image_issue_type}_issue"] == True].index.tolist()
    self.file_to_issue_map[image_issue_type] = list_of_offending_images

  def get_list_of_images_no_issues(self) -> List[str]:
    issue_types_found = self.image_examiner.issue_summary.query("num_images > 0")["issue_type"].tolist()
    print(f" issue_types_found : {issue_types_found}")
    for issue in issue_types_found:
      self.set_filenames_with_specific_issue(issue)

    self.images_no_issues = list(set(self.all_images) - set(list(self.file_to_issue_map.values())[0]))
    return self.images_no_issues

  def walk_direcotry_assign_labels_by_image_paths(self):
    """
    Walks through a directory and assigns labels to images based on their paths.

    """
    pass

  def labels_to_dataset(self):
    """
    Converts labels to dataset.

    Returns:
      A dataset of labels.
    """
    pass