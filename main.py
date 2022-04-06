import os
from turtle import color
import cv2
from uuid import uuid4
from matplotlib import image
import numpy as np
# import shutilppip
from os import path
import subprocess

scriptRootPath = path.abspath(path.abspath(path.dirname(__file__))+'//') + '//'
scriptRootPath = scriptRootPath.replace('//','\\')
print(scriptRootPath)

class color_class:

    def __init__(self,image):
        self.image = image
        self.image_name = image
        self.image_dict={}
        self.mapping = {
        0:'black',
        1:'blue',
        2:'brown',
        3:'green',
        4:'pink',
        5:'red',
        6:'white',
        7:'yellow'
    }
        
    
    def image_load(self):

        self.image = cv2.imread('cars\{}'.format(self.image))
        print(self.image)
        return self.image
    

    
    def predict(self):
        self.image = self.image_load()
       
        
        # Converting RGB channel to HSV.
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Set the range for different colors.
        black_mask = cv2.inRange(hsv,(0,0,0),(180,255,30))
        blue_mask = cv2.inRange(hsv,(100,150,0),(140,255,255))
        brown_mask = cv2.inRange(hsv,(10,100,20),(20,255,200))
        green_mask = cv2.inRange(hsv,(36,0,0),(70,255,255))
        pink_mask = cv2.inRange(hsv,(160,50,70),(180,255,255))
        red_mask1 = cv2.inRange(hsv,(0,100,20),(10,255,255))
        red_mask2 = cv2.inRange(hsv,(160,100,20),(179,255,255))
        red_mask = red_mask1 + red_mask2
        white_mask = cv2.inRange(hsv,(0,0,200),(0,0,255)) 
        yellow_mask = cv2.inRange(hsv,(15,0,0),(36,255,255))
        
        final = []
        masks = [black_mask,blue_mask,brown_mask,green_mask,pink_mask,red_mask,white_mask,yellow_mask]
        # loop over the boundaries
        for mask in masks:
            output = cv2.bitwise_and(self.image, self.image, mask=mask)

            final.append(np.count_nonzero(output))
        i = np.argmax(final)
        # print(final)
        print(i)        

        return i 
    
    def save_img(self,i):
        copyImage = subprocess.run('copy cars\{} {}\\'.format(self.image_name, self.mapping[i]), shell=True)
        print('copy cars\{} {}'.format(self.image_name, self.mapping[i]))
def main():
    status, listOfImage = subprocess.getstatusoutput('wsl ls cars'.format(scriptRootPath))
    print(listOfImage)
    # print('dir {}cars'.format(scriptRootPath))
    # print('a')
    # exit()
    for image in listOfImage.split('\n'):
        obj = color_class(image) 
        i = obj.predict()
        obj.save_img(i)

if __name__ == "__main__":
    main()
    