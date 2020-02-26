from skimage import metrics
import cv2 as cv
import numpy

class Reducer:

    score_holder = {}

    def __init__(self, input_images, max_num_return, focus_min_threshold=1000, previous_state_image=None, brightness_check=None):
        if self.validate_inputs(input_images,max_num_return, focus_min_threshold, previous_state_image, brightness_check) != ValueError:
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
        if type(self.input_images) != list or type(self.input_images[0]) != numpy.ndarray:
            raise ValueError("Inappropriate values provided as input image \nMust be list of numpy.ndarrays")

        if type(self.max_num_return) != int or self.max_num_return > len(self.input_images):
            raise ValueError("Inappropriate value provided as max_num_return \nMust be integer and less than len of input images")

        if type(self.focus_min_threshold) != int:
            raise ValueError("Inappropriate value provided as focus_threshold \nMust be integer")

        if type(self.previous_state_image) != numpy.ndarray and type(self.previous_state_image) != None:
            raise ValueError("Inappropriate values provided as previous image \nMust be type of numpy.ndarrays")

        if self.brightness_check != "PI" and (type(self.brightness_check) != int and self.brightness_check >= 0 and self.brightness_check <= 255):
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

        else:
            pass
    
    def sort_and_return_images(self):
        for index,score in self.score_holder.items():
            if score < self.focus_min_threshold:
                self.score_holder = self.score_holder[:index]
        
        final_image_scores = sorted(self.score_holder.items(), key=lambda kv:(kv[1], kv[0]), reverse = True)
            
        if len(final_image_scores) > self.max_num_return:
            final_image_scores = final_image_scores[:(self.max_num_return+1)]

        return final_image_scores
