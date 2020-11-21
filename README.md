# Frame-Reduction-Module
Module for reducing and providing best images by applying different filters from a bunch of frames provided to it

## Algorithms in Use
1. Variance of laplace : Inorder to detect blur within the images
2. The Structural SIMilarity (SSIM) : Inorder to check the similarity between images
3. Opencv Modules (color changing) : Inorder to check for brightness similarity between images

## How to use
1. Initialize the class with the frames captured by the camera. Options for providing the maximum number of images
   returned, minimum focus threashold, previous image state and brightness check can be added.
2. Call the get_images method on the class
