import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET


def table_detection(img_path, xml_path):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img_bin) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = cv2.bitwise_not(img_bin)
    #Draw bounded box from .xml data 
    tree = ET.parse(xml_path)

    root = tree.getroot()

    sample_annotations = []

    for neighbor in root.iter('bndbox'):
        xmin = int(neighbor.find('xmin').text)
        ymin = int(neighbor.find('ymin').text)
        xmax = int(neighbor.find('xmax').text)
        ymax = int(neighbor.find('ymax').text)

        sample_annotations.append((xmin, ymin, xmax, ymax))

    print(sample_annotations)

    img_annotated = img.copy()

    for bbox in sample_annotations:
        cv2.rectangle(img_annotated, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 1)

    cv2.imshow("img", img_annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # kernel_length_v = (np.array(img_gray).shape[1])//120
    # vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_v)) 
    # im_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    # vertical_lines_img = cv2.dilate(im_temp1, vertical_kernel, iterations=3)

    # kernel_length_h = (np.array(img_gray).shape[1])//40
    # horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_h, 1))
    # im_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    # horizontal_lines_img = cv2.dilate(im_temp2, horizontal_kernel, iterations=3)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # table_segment = cv2.addWeighted(vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    # table_segment = cv2.erode(cv2.bitwise_not(table_segment), kernel, iterations=2)
    # thresh, table_segment = cv2.threshold(table_segment, 0, 255, cv2.THRESH_OTSU)
   
    # contours, hierarchy = cv2.findContours(table_segment, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # count = 0
    # for c in contours:
    #     x, y, w, h = cv2.boundingRect(c)
    #     if (w > 80 and h > 20) and w > 3 * h:
    #         count += 1
    #         cropped = img[y:y + h, x:x + w]
            
    #         if True:
    #         	cv2.imwrite("./results/cropped/crop_" + str(count) + "__" + img_path.split('/')[-1], cropped)
    #     cv2.rectangle(img,(x, y),(x + w, y + h),(0, 255, 0), 1)

    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # if True:    
	#     cv2.imwrite("./results/table_detect/table_detect__" + img_path.split('/')[-1], table_segment)
	#     cv2.imwrite("./results/bb/bb__" + img_path.split('/')[-1], img)

for i in os.listdir('./forms/'):
    if i.endswith('.png') or i.endswith('.PNG') or i.endswith('.jpg') or i.endswith('.JPG'):
        table_detection(os.path.splitext('./forms/' + i)[0] + '.png', os.path.splitext('./forms/' + i)[0] + '.xml') # os.path.splitext use for split file name out of extension
