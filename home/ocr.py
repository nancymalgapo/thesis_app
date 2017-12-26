import pytesseract
from PIL import Image
from os.path import dirname, realpath
import glob
import pdb
import os

from .hcr import HCR
from .utils import format_list


DATASET_DIR = dirname(realpath(__file__)) + "/datasets/"
CLS_PATH = DATASET_DIR + 'classifications.txt'
FLT_PATH = DATASET_DIR + 'flattened_images.txt'


def read_handwritten_from_dir(dir_path):
    print 'Handwriting! Initializing HCR'
    hcr = HCR()
    hcr.load_trained_data(CLS_PATH, FLT_PATH)

    # Generate dir for scanned_images
    print '========= > Creating dir for %s/gen_images' % dir_path
    os.system('mkdir %s/gen_images' % dir_path)
    temp_list = []
    for f in glob.glob(dir_path + '/*.jpg'):
        unformatted_list = hcr.read_img(f)
        temp_list.append(format_list(unformatted_list))
    return temp_list


def read_typewritten_img(image_path):
    return pytesseract.image_to_string(Image.open(image_path))
