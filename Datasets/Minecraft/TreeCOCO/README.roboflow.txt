
Minecraft Tree Detection  - v1 TreeDetection
==============================

This dataset was exported via roboflow.com on June 25, 2024 at 8:17 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 5220 images.
Tree are annotated in COCO for MMDetection format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise
* Random shear of between -12° to +12° horizontally and -15° to +15° vertically
* Salt and pepper noise was applied to 1.97 percent of pixels


