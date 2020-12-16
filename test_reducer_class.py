import unittest
import os
import cv2
from reducer_class import Reducer

class TestReducer(unittest.TestCase):

    def test_return_length_1(self):
        imagesTest = getImagesForTest("./images", 20)
        reducerClass = Reducer(imagesTest, 5)
        reducedImageList = reducerClass.get_images()
        compareValue = len(reducedImageList)
        self.assertLessEqual(compareValue, 5)
    
    def test_return_length_2(self):
        imagesTest = getImagesForTest("./images", 5)
        reducerClass = Reducer(imagesTest, 5)
        reducedImageList = reducerClass.get_images()
        compareValue = len(reducedImageList)
        self.assertLessEqual(compareValue, 5)

    def test_values_1(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 51)

    def test_values_2(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 21)

    def test_values_3(self):
        imagesTest = 16
        self.assertRaises(ValueError, Reducer, imagesTest, 5)

    def test_values_4(self):
        imagesTest = "image"
        self.assertRaises(ValueError, Reducer, imagesTest, 6)

    def test_values_5(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, "Av")

    def test_values_6(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, "hi")

    def test_values_7(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 2.1)

    def test_optional_parameters_1(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 5, 1000, imagesTest[5], 122)

    def test_optional_parameters_2(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 5, 1000, imagesTest[5], -1)

    def test_optional_parameters_3(self):
        imagesTest = getImagesForTest("./images", 20)
        previous_state_image = 45
        self.assertRaises(ValueError, Reducer, imagesTest, 5, 1000, previous_state_image, 122)

    def test_optional_parameters_4(self):
        imagesTest = getImagesForTest("./images", 20)
        self.assertRaises(ValueError, Reducer, imagesTest, 5, "av", imagesTest[5], 122)

    def test_optional_parameters_5(self):
        imagesTest = "hello"
        previous_state_image = "image"
        self.assertRaises(ValueError, Reducer, imagesTest, "av", 1000, previous_state_image, -1)

    def test_optional_parameters_6(self):
        self.assertRaises(ValueError, Reducer,"","","","","")


def getImagesForTest(folder, size=0):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                images.append(img)
        
        if size == 0 or type(size) != int:
            return None
        return images[:size]


if __name__ == '__main__':
    unittest.main()

#python -m unittest