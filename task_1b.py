'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[544]
# Author List:		[Bhargav,Saketh,Jeevanandan,Sreekar]
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
# 					[order_points]
# Global variables:
# 					[i]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


def sort_12_points(elem):
    return elem[0]+elem[1]


def take_first(elem):
    return elem[0]


def take_second(elem):
    return elem[1]


def sort_12_points(elem):
    return elem[0]+elem[1]


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################
z = 0


def applyPerspectiveTransform_2(input_img):
    global z
    warped_img = None
    ret, thresh = cv2.threshold(input_img, 140, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    lst = []
    lst_m = []
    for cnt in contours:
        for i in range(len(cnt)):
            lst.append(cnt[i][0])
            sorted_list_x = sorted(lst, key=take_first, reverse=True)
            x_max = sorted_list_x[0]
            x_min = sorted_list_x[-1]
            sorted_list_y = sorted(lst, key=take_second, reverse=True)
            y_max = sorted_list_y[0]
            y_min = sorted_list_y[-1]
            top_left = [x_min[0], y_min[1]]
            top_right = [x_max[0], y_min[1]]
            bottom_right = [x_max[0], y_max[1]]
            bottom_left = [x_min[0], y_max[1]]
            lst_m.append(top_left)
            lst_m.append(top_right)
            lst_m.append(bottom_right)
            lst_m.append(bottom_left)
            lst = []
    sorted_list = sorted(lst_m, key=sort_12_points, reverse=True)
    top_left = sorted_list[-1]
    bottom_right = sorted_list[0]
    top_right = [bottom_right[0], top_left[1]]
    bottom_left = [top_left[0], bottom_right[1]]
    # print(top_left, top_right, bottom_right, bottom_left)
    pts = np.float32([[0, 0], [1280, 0], [1280, 1280], [0, 1280]])
    approx = np.float32([top_left, top_right, bottom_right, bottom_left])
    #approx = np.float32([[60, 70], [1215, 70], [1215, 1210], [60, 1210]])

    op = cv2.getPerspectiveTransform(approx, pts)
    warped_img = cv2.warpPerspective(input_img, op, (1280, 1280))

    approx = np.float32([[70, 70], [1215, 70], [1215, 1205], [70, 1205]])
    op = cv2.getPerspectiveTransform(approx, pts)
    warped_img = cv2.warpPerspective(warped_img, op, (1280, 1280))
    # cv2.imwrite("warped"+str(z)+".png", warped_img)
    # z += 1
    return warped_img
##############################################################


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    pts = pts.reshape((4, 2))
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def applyPerspectiveTransform(input_img):
    warped_img = None

    # """
    # Purpose:
    # ---
    # takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

    # Input Arguments:
    # ---
    # `input_img` :   [ numpy array ]
    # 	maze image in the form of a numpy array

    # Returns:
    # ---
    # `warped_img` :  [ numpy array ]
    # 	resultant warped maze image after applying Perspective Transform

    # Example call:
    # ---
    # warped_img = applyPerspectiveTransform(input_img)
    # """

    ##############	ADD YOUR CODE HERE	##############
    # cv2.imwrite("Imgeee"+str(i)+".png",input_img)

    img_grey = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_grey, 120, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)
    dila = cv2.dilate(thresh, kernel, iterations=3)
    ero = cv2.erode(dila, kernel, iterations=3)
    img_gua = cv2.GaussianBlur(ero, (5, 5), 0.5)
    # img_can = cv2.Canny(img_gua, 40, 50)
    # img_gua = cv2.GaussianBlur(ero, (5, 5), 0.5)
    # img_can = cv2.Canny(img_gua, 40, 50)
# cv2.imwrite('cont.png', img_can)
    contours, hi = cv2.findContours(
        img_gua, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    target = 0
    for con in contours:
        approx = cv2.approxPolyDP(con, 0.02*cv2.arcLength(con, True), True)
        if len(approx) == 4:
            target = approx
            break
    approx = order_points(target)
    # print(approx)
    pts = np.float32([[0, 0], [300, 0], [300, 300], [0, 300]])
    # print(pts)
    op = cv2.getPerspectiveTransform(approx, pts)
    warped_img = cv2.warpPerspective(ero, op, (305, 305))

    ##################################################

    return warped_img


def detectMaze(warped_img):

    # """
    # Purpose:
    # ---
    # takes the warped maze image as input and returns the maze encoded in form of a 2D array

    # Input Arguments:
    # ---
    # `warped_img` :    [ numpy array ]
    # 	resultant warped maze image after applying Perspective Transform

    # Returns:
    # ---
    # `maze_array` :    [ nested list of lists ]
    # 	encoded maze in the form of a 2D array

    # Example call:
    # ---
    # maze_array = detectMaze(warped_img)
    # """

    maze_array = []

    ##############	ADD YOUR CODE HERE	##############
    kernel = np.ones((5, 5), np.uint8)
    dialt = cv2.dilate(warped_img, kernel, iterations=1)
    top, bottom, right, left = 0, 0, 0, 0
    su = 0
    k = 0
    l = 0
    lst = []

    for i in range(10):
        for j in range(10):
            img_copy = dialt[k:k+31, l:l+31]
            if (img_copy.any()):
                img_resize = cv2.resize(img_copy, (500, 500))
            if((img_resize[40, 250] > 200).any()):
                top = 2
            if(((img_resize[300, 20] > 200) or (img_resize[250, 1] > 200)).any()):
                left = 1
            if((img_resize[250, 495] == 255).any()):
                right = 4
            if((img_resize[495, 250] == 255).any()):
                bottom = 8
            su = top+left+right+bottom
            lst.append(su)
            top = 0
            right = 0
            left = 0
            bottom = 0
            l += 30
        k += 30
        maze_array.append(lst)
        lst = []
        l = 0

        ##################################################

    return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.
if __name__ == "__main__":

    # path directory of images in 'test_cases' folder
    img_dir_path = 'test_cases/'

    # path to 'maze00.jpg' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # path for 'maze00.csv' output file
    csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            # writes the encoded maze array to the csv file
            writeToCsv(csv_file_path, maze_array)

            cv2.imshow('warped_img_0' + str(file_num), warped_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:

            print(
                '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
            exit()

    else:

        print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
        exit()

    choice = input(
        '\nDo you want to run your script on all maze images ? => "y" or "n": ')

    if choice == 'y':

        for file_num in range(1, 10):

            # path to image file
            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # path for csv output file
            csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'

            # read the image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    # writes the encoded maze array to the csv file
                    writeToCsv(csv_file_path, maze_array)

                    cv2.imshow('warped_img_0' + str(file_num), warped_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

                else:

                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:

                print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:

        print('')
