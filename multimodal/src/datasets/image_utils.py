import os
import pandas as pd
from typing import List, Set

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
    self.images_no_issues = None
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

  def labels_to_dataset(self):
    """
    Converts labels to dataset.

    Returns:
      A dataset of labels.
    """
    pass

  def _remove_prefix_from_set(self, original_set, prefix="/content/images/") -> Set:
    """Removes the given prefix from each string in the set.

    Args:
      original_set: The set of strings.
      prefix: The prefix to remove.

    Returns:
      A new set with the prefix removed from each string.
    """
    return {s[len(prefix):] if s.startswith(prefix) else s for s in original_set}
