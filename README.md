# multimodal-sdk


### Find common issues with images
Here is a list of the common image issue types this SDK supports:

| Issue Type | Issue Description 2 | Issue Key |
|---|---|---|
| Light | Images that are too bright/washed out in the dataset | light|
|Dark |Images that are irregularly dark | dark|
|Odd Aspect Ratio |Images with an unusual aspect ratio (i.e. overly skinny/wide) | odd_aspect_ratio|
|Exact Duplicates |Images that are exact duplicates of each other | exact_duplicates|
|Near Duplicates |Images that are almost visually identical to each other (e.g. same image with different filters) | near_duplicates|
|Blurry |Images that are blurry or out of focus | blurry|
|Grayscale |Images that are grayscale (lacking color) | grayscale|
|Low Information |Images that lack much information (e.g. a completely black image with a few white dots) | low_information|
|Odd Size |Images that are abnormally large or small compared to the rest of the dataset | aodd_size|

Sample Usage...
```
img_utils = ImageUtils(image_dir = "./images")
img_utils.find_images_in_directory()
img_utils.find_issues_in_images()
issue_types_found = img_utils.report_image_issue_types_found()

img_utils.get_list_of_images_no_issues()
```