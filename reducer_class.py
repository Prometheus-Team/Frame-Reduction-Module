from skimage import metrics
import cv2 as cv
import numpy
# Testing images
from imutils import paths
import argparse

class Reducer:

    score_holder = {}

    def __init__(self, input_images, max_num_return, focus_min_threshold=1000, previous_state_image=None, brightness_check=None):
            self.validate_inputs(input_images,max_num_return, focus_min_threshold, previous_state_image, brightness_check)
            self.input_images = input_images
            self.max_num_return = max_num_return
            self.focus_min_threshold = focus_min_threshold
            self.previous_state_image = previous_state_image
            self.brightness_check = brightness_check    

    def get_images(self):
        self.calculate_focus()
        self.check_image_similarity()
        self.check_brightness_similarity()
        return self.sort_and_return_images()

    def validate_inputs(self, input_images, max_num_return, focus_min_threshold, previous_state_image, brightness_check):
        # if type(self.input_images) != list or type(self.input_images[0]) != numpy.ndarray:
        if type(input_images) != list or type(input_images[0] != numpy.ndarray):
            raise ValueError("Inappropriate values provided as input image \nMust be list of numpy.ndarrays")

        if type(max_num_return) != int or max_num_return > len(input_images):
            raise ValueError("Inappropriate value provided as max_num_return \nMust be integer and less than len of input images")

        if len(input_images) < max_num_return:
            raise ValueError("Size of reutrned images is greater than the number of images provided")

        if type(focus_min_threshold) != int:
            raise ValueError("Inappropriate value provided as focus_threshold \nMust be integer")

        if previous_state_image != None and type(previous_state_image) != numpy.ndarray:
            raise ValueError("Inappropriate values provided as previous image \nMust be type of numpy.ndarray")

        if previous_state_image != None and type(brightness_check) != int and (type(brightness_check) == int and (brightness_check < 0 or brightness_check > 255)):
            raise ValueError("Inappropriate values provided as brightness check \nMust be type 'PI' or integer valuein the range of 0-255")

    def variance_of_laplacian(self, image):
        return cv.Laplacian(image, cv.CV_64F).var()

    def calculate_focus(self):
        self.score_holder = {}
        for index, image in enumerate(self.input_images):
            grayed_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            focus_score = self.variance_of_laplacian(grayed_image)
            self.score_holder[index] = focus_score

    def check_image_similarity(self):
        if self.previous_state_image != None:
            for index, image in enumerate(self.input_images):
                ssim_similarity = metrics.structural_similarity(image, self.previous_state_image, multichannel=True)
                self.score_holder[index] = self.score_holder[index] * (1 - ssim_similarity)
    
    def check_brightness_similarity(self):
        if(self.brightness_check != None):
            if type(self.brightness_check) == int:
                for index, image in enumerate(self.input_images):
                    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
                    image_hsv_value = cv.mean(image_hsv)[2]
                    self.score_holder[index] = self.score_holder[index] * (1 / abs(self.brightness_check - image_hsv_value))

            elif self.brightness_check == "PI":
                pre_image_hsv = cv.cvtColor(self.previous_state_image, cv.COLOR_BGR2HSV)
                pre_image_hsv_value = cv.mean(pre_image_hsv)[2]
                for index, image in enumerate(self.input_images):
                    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
                    image_hsv_value = cv.mean(image_hsv)[2]
                    self.score_holder[index] = self.score_holder[index] * (1 / abs(pre_image_hsv_value - image_hsv_value))
    
    def sort_and_return_images(self):
        toberemovedindex = []
        for index,score in self.score_holder.items():
            if score <= self.focus_min_threshold:
                toberemovedindex.append(index)

        for index in toberemovedindex:
            del self.score_holder[index]
        
        final_image_scores = sorted(self.score_holder.items(), key=lambda kv:(kv[1], kv[0]), reverse = True)

        if len(final_image_scores) > self.max_num_return:
            final_image_scores = final_image_scores[:(self.max_num_return)]

        returnedImageList = []
        for tupleValues in final_image_scores:
            returnedImageList.append([self.input_images[tupleValues[0]],tupleValues[0],tupleValues[1]])

        return returnedImageList


if __name__ == "__main__":
    # import images
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
    args = vars(ap.parse_args())
    # loop over the input images
    imagesList = []
    for imagePath in paths.list_images(args["images"]):
        imagesList.append(cv.imread(imagePath))

    reducerClass = Reducer(imagesList, 5)
    images = reducerClass.get_images()
    print(type(images[0][0]))
    cv.imshow("image1",images[0][0])
    cv.imshow("image2",reducerClass.input_images[2])
    cv.waitKey(0)