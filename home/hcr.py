#!/usr/bin/env python

import cv2
import numpy as np
import sys
import pytesseract
from PIL import Image as img_pil
import os


MIN_CONTOUR_AREA = 100
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

CLASSIFICATIONS_PATH = 'classifications.txt'
FLATTENED_IMG_PATH = 'flattened_images.txt'

PATH = 'datasets/'

# Allowed characters for text recognition
# As of now, im only using A-Z as expected characters
UCASE_LETTERS = range(ord('A'), ord('Z') + 1)
LCASE_LETTERS = range(ord('a'), ord('z') + 1)
ALLCASE_LETTERS = UCASE_LETTERS + LCASE_LETTERS

NUMBERS = range(ord('0'), ord('9') + 1)
UCASE_NUMERIC = NUMBERS + UCASE_LETTERS
LCASE_NUMERIC = NUMBERS + LCASE_LETTERS

ALPHA_NUMERIC = NUMBERS + ALLCASE_LETTERS

# Allowed characters for text recognition
# As of now, im only using A-Z as expected characters
EXPECTED_CHARS = range(ord('A'), ord('Z') + 1)


class ContourWithData():
    npaContour, boundingRect = None, None
    intRectX, intRectY, intRectWidth, intRectHeight = 0, 0, 0, 0
    fltArea = 0.0

    def calculateRectTopLeftPointAndWidthAndHeight(self):
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA:
            return False
        return True


class HCR():

    def __init__(self):
        self.csf_path = None
        self.flat_img_path = None
        self.npaClassifications = None
        self.npaFlattenedImages = None
        self.kNearest = None

    def load_trained_data(
            self,
            csf_path=CLASSIFICATIONS_PATH,
            flat_img_path=FLATTENED_IMG_PATH):
        try:
            self.npaClassifications = np.loadtxt(csf_path, np.float32)
            self.npaFlattenedImages = np.loadtxt(flat_img_path, np.float32)

            self.npaClassifications = self.npaClassifications.reshape(
                (self.npaClassifications.size, 1))

            # Train data
            self.kNearest = cv2.ml.KNearest_create()
            self.kNearest.train(
                self.npaFlattenedImages,
                cv2.ml.ROW_SAMPLE,
                self.npaClassifications)
        except:
            print ('Unable to load the data! Exiting..')
            sys.exit()

    # Apply preprocessing to image.
    # This includes grayscale, blurring and applying thresh
    def preprocess_img(self, img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)

        imgThresh = cv2.adaptiveThreshold(
            imgBlurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2)
        return imgThresh

    def find_contours(self, img):
        return cv2.findContours(
            img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    """
        NOTE:
        This function generates `classifications.txt` and
        `flattened_images.txt` used for training data for your HCR.
        This method should only be run once unless you intended to
        generate new files for your training data.
    """

    def generate_train_data(self, img_path):
        imgTrainingNumbers = cv2.imread(img_path)

        if imgTrainingNumbers is None:
            print ('File not loaded! Exiting ...')
            sys.exit()

        # Apply pre-processing (grayscale, blurr, thresh)
        imgThresh = self.preprocess_img(imgTrainingNumbers)
        imgThreshCopy = imgThresh.copy()

        # Find contours on imgThreshCopy
        imgContours, npaContours, npaHierarchy = self.find_contours(
            imgThreshCopy)

        npaFlattenedImages = np.empty(
            (0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

        intClassifications = []
        for npaContour in npaContours:
            if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
                [intX, intY, intW, intH] = cv2.boundingRect(npaContour)

                imgROI = imgThresh[intY:intY + intH, intX:intX + intW]
                imgROIResized = cv2.resize(
                    imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

                cv2.imshow("imgROI", imgROI)

                # Wait for user input to determine the recognized char
                intChar = cv2.waitKey(0)

                # If `esc` is pressed, exit the program
                if intChar == 27:
                    sys.exit()
                # If key is in expected characters, save
                elif intChar in EXPECTED_CHARS:
                    intClassifications.append(intChar)
                    npaFlattenedImage = imgROIResized.reshape(
                        (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                    npaFlattenedImages = np.append(
                        npaFlattenedImages, npaFlattenedImage, 0)

        fltClassifications = np.array(intClassifications, np.float32)
        npaClassifications = fltClassifications.reshape(
            (fltClassifications.size, 1))

        print ("\nTraining complete! files are generated on current dir\n")

        # Generate files in the current directory
        np.savetxt(PATH + "/classifications.txt", npaClassifications)
        np.savetxt(PATH + "/flattened_images.txt", npaFlattenedImages)
        cv2.destroyAllWindows()

    def put_txt(self, img, text, x, y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            img, text, (x, y), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def read_img(self, img_path):
        imgTestingNumbers = cv2.imread(img_path)

        allContoursWithData = []
        validContoursWithData = []

        if imgTestingNumbers is None:
            print ('error: image not read from file \n\n')
            sys.exit()

        # Create blank image for output
        srcHeight, srcWidth = imgTestingNumbers.shape[:2]
        outputImg = np.zeros((srcHeight, srcWidth, 4), np.uint8)
        outputImg.fill(255)

        imgThresh = self.preprocess_img(imgTestingNumbers)
        imgThreshCopy = imgThresh.copy()

        imgContours, npaContours, npaHierarchy = self.find_contours(
            imgThreshCopy)

        for npaContour in npaContours:
            contourWithData = ContourWithData()
            contourWithData.npaContour = npaContour
            contourWithData.boundingRect = cv2.boundingRect(
                contourWithData.npaContour)
            contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
            contourWithData.fltArea = cv2.contourArea(
                contourWithData.npaContour)
            allContoursWithData.append(contourWithData)

        for c in allContoursWithData:
            if c.checkIfContourIsValid():
                validContoursWithData.append(c)

        for c in validContoursWithData:
            imgROI = imgThresh[
                c.intRectY: c.intRectY + c.intRectHeight,
                c.intRectX: c.intRectX + c.intRectWidth]

            # cv2.rectangle(
            #     imgTestingNumbers,
            #     (c.intRectX, c.intRectY),
            #     (c.intRectX + c.intRectWidth, c.intRectY + c.intRectHeight),
            #     (0, 255, 0),
            #     2)

            imgROIResized = cv2.resize(
                imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

            # Show detected character
            # cv2.imshow("Detected character", imgROIResized)

            npaROIResized = imgROIResized.reshape(
                (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

            npaROIResized = np.float32(npaROIResized)

            retval, npaResults, neigh_resp, dists = self.kNearest.findNearest(
                npaROIResized, k=5)

            # print retval, npaResults, neigh_resp, dists
            strCurrentChar = str(chr(int(npaResults[0][0])))

            self.put_txt(
                outputImg,
                strCurrentChar,
                c.intRectX,
                c.intRectY + c.intRectHeight)

            # cv2.imshow("imgTestingNumbers", imgTestingNumbers)
            # cv2.waitKey(0)

        # Create new temp image for pytesseract
        # cv2.imshow("imgTestingNumbers", outputImg)    
        # cv2.waitKey(0)

        # img_arr = img_pil.fromarray(outputImg)


        # Saved temp images to generated dir
        dirname = os.path.dirname(img_path)
        basename = os.path.basename(img_path)
        tmp_name = basename[:basename.find('.')] + '-tmp.jpg'
        cv2.imwrite('%s/gen_images/%s' % (dirname, tmp_name), outputImg)
        # return pytesseract.image_to_string(img_arr)

        return pytesseract.image_to_string(img_pil.open('img-temp.jpg'))

        # cv2.imshow("imgTestingNumbers", imgTestingNumbers)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()
        # return
