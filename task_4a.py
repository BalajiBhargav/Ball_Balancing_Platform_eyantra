'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 4A of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Filename:			task_4a.py
# Functions:		find_path, read_start_end_coordinates
# 					[astar]
# Global variables:
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the six available   ##
## modules for this task (numpy, opencv, os, traceback,     ##
## sys, json)												##
##############################################################
import numpy as np
import cv2
import os
import traceback
import sys
import json


# Import 'task_1b.py' file as module
try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')
    sys.exit()

except Exception as e:
    print('Your task_1b.py throwed an Exception, kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)
    sys.exit()

##############################################################
import operator

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


class Node:
    def __init__(self, parent, position):
        self.parent = None
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0


def withinrage(p_x, p_y, maze_array):
    # within_range_criteria = [
    #         p_x > (len(maze_array) - 1),
    #         p_x< 0,
    #         p_y > (len(maze_array[len(maze_array) - 1]) - 1),
    #         p_y< 0,
    #     ]
    if (p_x > (len(maze_array) - 1) or (p_x < 0) or (p_y > (len(maze_array[len(maze_array) - 1]) - 1)) or (p_y < 0)):
        return True
    else:
        return False


def astar(start_coord, end_coord, maze_array):
    openset = []
    closedset = []
    print(start_coord)
    start_node = Node(None, tuple(start_coord))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end_coord))
    end_node.g = end_node.h = end_node.f = 0

    openset.append(start_node)

    while len(openset) > 0:
        # current_node = sorted(openset, key=operator.attrgetter(f))
        # current_node=openset[0]
        # for item in openset:
        #     print("openset", item.position)
        # for item in closedset:
        #     print("closedset", item.position)
        current_node = min(openset, key=lambda o: o.f)
        # for index, item in enumerate(openset):
        #     if item.f < current_node.f:
        #         current_node = item
        #         current_index = index
        if current_node.position == end_node.position:
            path = []
            while current_node.parent:
                path.append(current_node.position)
                current_node = current_node.parent
            path.append(current_node.position)
            return path[::-1]

        openset.remove(current_node)
        closedset.append(current_node)
        # print("currentnode", current_node.position)
        pos = current_node.position
        val = maze_array[pos[0]][pos[1]]
        # print(val)
        children = []
        if val == 7:
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            p = (p_x_d, p_y_d)
            new_node_1 = Node(current_node, p)
            children.append(new_node_1)
        if val == 3:
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            p2 = (p_x_r, p_y_r)
            new_node_2 = Node(current_node, p2)
            children.append(new_node_2)
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            p3 = (p_x_d, p_y_d)
            new_node_3 = Node(current_node, p3)
            children.append(new_node_3)
        if val == 10:
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            p4 = (p_x_r, p_y_r)
            new_node_4 = Node(current_node, p4)
            children.append(new_node_4)
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            p5 = (p_x_l, p_y_l)
            new_node_5 = Node(current_node, p5)
            children.append(new_node_5)
        if val == 14:
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            p6 = (p_x_l, p_y_l)
            new_node_6 = Node(current_node, p6)
            children.append(new_node_6)
        if val == 6:
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            p7 = (p_x_l, p_y_l)
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            new_node_7 = Node(current_node, p7)
            children.append(new_node_7)
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p8 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_8 = Node(current_node, p8)
            children.append(new_node_8)
        if val == 5:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p9 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_9 = Node(current_node, p9)
            children.append(new_node_9)
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p10 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_10 = Node(current_node, p10)
            children.append(new_node_10)
        if val == 8:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p11 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_11 = Node(current_node, p11)
            children.append(new_node_11)
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            p12 = (p_x_l, p_y_l)
            new_node_12 = Node(current_node, p12)
            children.append(new_node_12)
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            p13 = (p_x_r, p_y_r)
            new_node_13 = Node(current_node, p13)
            children.append(new_node_13)
        if val == 9:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p14 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_14 = Node(current_node, p14)
            children.append(new_node_14)
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            p15 = (p_x_r, p_y_r)
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            new_node_15 = Node(current_node, p15)
            children.append(new_node_15)
        if val == 11:
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            p16 = (p_x_r, p_y_r)
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            new_node_16 = Node(current_node, p16)
            children.append(new_node_16)
        if val == 12:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p17 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_17 = Node(current_node, p17)
            children.append(new_node_17)
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            p18 = (p_x_l, p_y_l)
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            new_node_18 = Node(current_node, p18)
            children.append(new_node_18)
        if val == 13:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p19 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_19 = Node(current_node, p19)
            children.append(new_node_19)
        if val == 15:
            pass
        if val == 4:
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p21 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_21 = Node(current_node, p21)
            children.append(new_node_21)
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            p22 = (p_x_l, p_y_l)
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            new_node_22 = Node(current_node, p22)
            children.append(new_node_22)
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p23 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_23 = Node(current_node, p23)
            children.append(new_node_23)
        if val == 2:
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            p24 = (p_x_l, p_y_l)
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            new_node_24 = Node(current_node, p24)
            children.append(new_node_24)
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p25 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_25 = Node(current_node, p25)
            children.append(new_node_25)
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            p26 = (p_x_r, p_y_r)
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            new_node_26 = Node(current_node, p26)
            children.append(new_node_26)
        if val == 1:
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p27 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_27 = Node(current_node, p27)
            children.append(new_node_27)
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            p28 = (p_x_r, p_y_r)
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            new_node_28 = Node(current_node, p28)
            children.append(new_node_28)
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p29 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_29 = Node(current_node, p29)
            children.append(new_node_29)
        if val == 0:
            p_x_d = pos[0]+1
            p_y_d = pos[1]
            p30 = (p_x_d, p_y_d)
            if withinrage(p_x_d, p_y_d, maze_array) == True:
                continue
            new_node_30 = Node(current_node, p30)
            children.append(new_node_30)
            p_x_r = pos[0]
            p_y_r = pos[1]+1
            p31 = (p_x_r, p_y_r)
            if withinrage(p_x_r, p_y_r, maze_array) == True:
                continue
            new_node_31 = Node(current_node, p31)
            children.append(new_node_31)
            p_x_t = pos[0]-1
            p_y_t = pos[1]
            p32 = (p_x_t, p_y_t)
            if withinrage(p_x_t, p_y_t, maze_array) == True:
                continue
            new_node_32 = Node(current_node, p32)
            children.append(new_node_32)
            p_x_l = pos[0]
            p_y_l = pos[1]-1
            p34 = (p_x_l, p_y_l)
            if withinrage(p_x_l, p_y_l, maze_array) == True:
                continue
            new_node_34 = Node(current_node, p34)
            children.append(new_node_34)
        for node in children:
            if len([closed_child for closed_child in closedset if closed_child.position == node.position]) > 0:
                continue

            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current_node.g + 10
                if node.g > new_g:
                    # If so, update the node to have a new parent
                    node.g = new_g
                    node.f = node.g+node.h
                    node.parent = current_node
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.g = current_node.g + 10
                node.h = abs((end_coord[0]-node.position[0])
                             * 10+abs(end_coord[1]-node.position[1])*10)
                # Set the parent to our current item
                node.f = node.g+node.h
                node.parent = current_node
                # Add it to the set
                openset.append(node)


##############################################################
def find_path(maze_array, start_coord, end_coord):
    """
    Purpose:
    ---
    Takes a maze array as input and calculates the path between the
    start coordinates and end coordinates.

    Input Arguments:
    ---
    `maze_array` :   [ nested list of lists ]
            encoded maze in the form of a 2D array

    `start_coord` : [ tuple ]
            start coordinates of the path

    `end_coord` : [ tuple ]
            end coordinates of the path

    Returns:
    ---
    `path` :  [ list of tuples ]
            path between start and end coordinates

    Example call:
    ---
    path = find_path(maze_array, start_coord, end_coord)
    """

    path = None

    ################# ADD YOUR CODE HERE #################
    path = astar(start_coord, end_coord, maze_array)
    ######################################################

    return path


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

    file_num = 0

    maze_name = 'maze0' + str(file_num)

    # path to 'maze00.jpg' image file
    img_file_path = img_dir_path + maze_name + '.jpg'

    # read start and end coordinates from json file
    start_coord, end_coord = read_start_end_coordinates(
        "start_end_coordinates.json", maze_name)

    print('\n============================================')
    print('\nFor maze0' + str(file_num) + '.jpg')

    # read the 'maze00.jpg' image file
    input_img = cv2.imread(img_file_path)

    # get the resultant warped maze image after applying Perspective Transform
    warped_img = task_1b.applyPerspectiveTransform(input_img)

    if type(warped_img) is np.ndarray:

        # get the encoded maze in the form of a 2D array
        maze_array = task_1b.detectMaze(warped_img)

        if (type(maze_array) is list) and (len(maze_array) == 10):

            print('\nEncoded Maze Array = %s' % (maze_array))
            print('\n============================================')

            path = find_path(maze_array, start_coord, end_coord)

            if (type(path) is list):

                print('\nPath calculated between %s and %s is %s' %
                      (start_coord, end_coord, path))
                print('\n============================================')

            else:
                print('\n Path does not exist between %s and %s' %
                      (start_coord, end_coord))

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

            maze_name = 'maze0' + str(file_num)

            img_file_path = img_dir_path + maze_name + '.jpg'

            # read start and end coordinates from json file
            start_coord, end_coord = read_start_end_coordinates(
                "start_end_coordinates.json", maze_name)

            print('\n============================================')
            print('\nFor maze0' + str(file_num) + '.jpg')

            # read the 'maze00.jpg' image file
            input_img = cv2.imread(img_file_path)

            # get the resultant warped maze image after applying Perspective Transform
            warped_img = task_1b.applyPerspectiveTransform(input_img)

            if type(warped_img) is np.ndarray:

                # get the encoded maze in the form of a 2D array
                maze_array = task_1b.detectMaze(warped_img)

                if (type(maze_array) is list) and (len(maze_array) == 10):

                    print('\nEncoded Maze Array = %s' % (maze_array))
                    print('\n============================================')

                    path = find_path(maze_array, start_coord, end_coord)

                    if (type(path) is list):

                        print('\nPath calculated between %s and %s is %s' %
                              (start_coord, end_coord, path))
                        print('\n============================================')

                    else:
                        print('\n Path does not exist between %s and %s' %
                              (start_coord, end_coord))

                else:
                    print(
                        '\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
                    exit()

            else:
                print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
                exit()

    else:
        print()
