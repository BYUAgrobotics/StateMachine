# OpencvPlantRecognition

# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt

# img = cv.imread('Data/plant1.png')
# assert img is not None, "file could not be read, check with os.path.exists()"
# b,g,r = cv.split(img)
# while True:
#     cv.imshow('img',img)
#     cv.imshow('r',r)
#     cv.imshow('b',b)
#     cv.imshow('g',g)

# hue saturation value for flowers then sick leaves and healthy leaves
# (hMin = 34 , sMin = 0, vMin = 176), (hMax = 179 , sMax = 49, vMax = 255) flowers
# (hMin = 20 , sMin = 66, vMin = 30), (hMax = 104 , sMax = 157, vMax = 125)healthy leaves
# (hMin = 53 , sMin = 63, vMin = 131), (hMax = 66 , sMax = 106, vMax = 218) sick leaves
#     k = cv.waitKey(5) & 0xFF
#     if k == 27:
#         break

# example of slider value tuner
import cv2
import numpy as np

def num_items(hsv, high, low, area,erosions=0,dilations=0):
    mask = cv2.inRange(hsv, low, high)

    mask = cv2.dilate(mask, None,iterations=dilations)
    mask = cv2.erode(mask, None,iterations=erosions)

    contours,hierarchy = cv2.findContours(mask, 1, 2)
    items = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > area:
            items += 1
    return items

# Load in image
image = cv2.imread('Data/plant2.png')
output = cv2.imread('Data/plant2.png')

# flower hsv
flower_low = np.array([90, 0, 176])
flower_hig = np.array([179, 74, 255])
# healthy leaf hsv
healthy_low = np.array([20, 66, 30])
healthy_hig = np.array([104, 157, 125])
# sick leaf hsv
sick_low = np.array([53, 63, 131])
sick_hig = np.array([66, 106, 218])

wait_time = 33
while(1):
    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # for a flower
    flowers = num_items(hsv, flower_hig, flower_low, 3000,erosions=0,dilations=0)
    print(flowers)
    flower_mask = cv2.inRange(hsv, flower_low, flower_hig)
    
    flower_mask = cv2.erode(flower_mask, None,1)
    # flower_output = cv2.bitwise_and(image,image, mask= flower_mask)
    # ret,thresh = cv2.threshold(flower_mask,127,255,0)
    contours,hierarchy = cv2.findContours(flower_mask, 1, 2)
    # flower_mask_cnt = contours[0]
    for cnt in contours:
        if cv2.contourArea(cnt) > 3000:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(flower_mask,(x,y),(x+w,y+h),(0,255,0),2)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)  
            cv2.drawContours(output,[box],0,(0,0,255),2)


    # for healthy leaves
    healthy_mask = cv2.inRange(hsv, healthy_low, healthy_hig)
    # # healthy_output = cv2.bitwise_and(image,image, mask= healthy_mask)
    healthy = num_items(hsv, healthy_hig, healthy_low, area=3000, erosions=5,dilations=3)
    print(healthy)
    healthy_mask = cv2.inRange(hsv, healthy_low, healthy_hig)
    erosion_size = 3
    erosion_shape = 1 #rectangle
    element = cv2.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1), (erosion_size, erosion_size))
    
    healthy_mask = cv2.dilate(healthy_mask, None,iterations=3)
    healthy_mask = cv2.erode(healthy_mask, None,iterations=5)
    contours,hierarchy = cv2.findContours(healthy_mask, 1, 2)
    for cnt in contours:
        if cv2.contourArea(cnt) > 3000:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(healthy_mask,(x,y),(x+w,y+h),(0,255,0),2)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)  
            cv2.drawContours(output,[box],0,(0,0,255),2)
    
    # for sick leaves
    sick_mask = cv2.inRange(hsv, flower_low, sick_hig)
    # sick_output = cv2.bitwise_and(image,image, mask= sick_mask)
    sick = num_items(hsv, sick_hig, sick_low, 1500,erosions=0,dilations=1)
    print(sick)
    sick_mask = cv2.inRange(hsv, sick_low, sick_hig)
    
    sick_mask = cv2.dilate(sick_mask, None,iterations=1)
    # sick_mask = cv2.erode(sick_mask, None,iterations=1)
    contours,hierarchy = cv2.findContours(sick_mask, 1, 2)
    for cnt in contours:
        if cv2.contourArea(cnt) > 1500:
            # print(cv2.contourArea(cnt))
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(sick_mask,(x,y),(x+w,y+h),(0,255,0),2)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)  
            cv2.drawContours(output,[box],0,(0,0,255),2)


    # Display output image
    cv2.imshow('flower_output_rgb', output)
    cv2.imshow('flower_output', flower_mask)
    cv2.imshow('healthy_output',healthy_mask)
    cv2.imshow('sick_output',   sick_mask)


    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(wait_time) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

