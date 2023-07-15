'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 5 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:          [ Team-ID ]
# Author List:      [ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:         task_5.py
# Functions:
#                   [ Comma separated list of functions in this file ]
# Global variables:
# 					[ List of global variables defined in this file ]

# NOTE: Make sure you do NOT call sys.exit() in this code.

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
import os
import sys
import traceback
import time
import math
import json

##############################################################
global maze_array_4, maze_array_1, maze_array_2, maze_array_3, revolute_handle_yz_t4, revolute_handle_xz_t4, revolute_handle_yz_t1, revolute_handle_xz_t1, filename, data, g, t4_handle, t1_handle, t2_handle, t3_handle
global revolute_handle_yz_t2, revolute_handle_xz_t2, revolute_handle_yz_t3, revolute_handle_xz_t3, vision_sensor_handle_4, vision_sensor_handle_3, vision_sensor_handle_2, vision_sensor_handle_1, vision_sensor_handle_5
g = 0
global dic

# Importing the sim module for Remote API connection with CoppeliaSim
try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')


# Import 'task_1b.py' file as module
try:
    import task_1b

except ImportError:
    print('\n[ERROR] task_1b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_1b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_2a.py' file as module
try:
    import task_2a

except ImportError:
    print('\n[ERROR] task_2a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_2b.py' file as module
try:
    import task_2b

except ImportError:
    print('\n[ERROR] task_2b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_2b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_2b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_3.py' file as module
try:
    import task_3

except ImportError:
    print('\n[ERROR] task_3.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_3.py is present in this current directory.\n')


except Exception as e:
    print('Your task_3.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


# Import 'task_4a.py' file as module
try:
    import task_4a

except ImportError:
    print('\n[ERROR] task_4a.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_4a.py is present in this current directory.\n')


except Exception as e:
    print('Your task_4a.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

# Import 'task_4b.py' file as module
try:
    import task_4b

except ImportError:
    print('\n[ERROR] task_4b.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure task_4b.py is present in this current directory.\n')


except Exception as e:
    print('Your task_4b.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)

##############################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    send_color_and_collection_box_identified
#        Inputs:    ball_color and collection_box_name
#       Outputs:    None
#       Purpose:    1. This function should only be called when the task is being evaluated using
# 					   test executable.
#					2. The format to send the data is as follows:
#					   'color::collection_box_name'
def send_color_and_collection_box_identified(ball_color, collection_box_name):

    global client_id

    color_and_cb = [ball_color + '::' + collection_box_name]
    inputBuffer = bytearray()
    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id, 'evaluation_screen_respondable_1',
                                                                                        sim.sim_scripttype_childscript, 'color_and_cb_identification', [], [], color_and_cb, inputBuffer, sim.simx_opmode_blocking)

################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################


def invert_model_properties(object_handle):
    # NOTE: This function will be used to invert model properties such that the model which is not to be
    # 		traversed in the current iteration can be partially disabled thereby saving the computational
    #		resources.

    global client_id
    return_code, curr_model_prop = sim.simxGetModelProperty(
        client_id, object_handle, sim.simx_opmode_blocking)
    if(curr_model_prop == 0):
        # Overrides the required model props as NOT measureable, NOT dynamic, NOT collidable, NOT
        # renderable, NOT detectable, NOT respondable and Invisible to other model's bounding boxes.
        return_code = sim.simxSetModelProperty(
            client_id, object_handle, 1135, sim.simx_opmode_blocking)
    else:
        return_code = sim.simxSetModelProperty(
            client_id, object_handle, 0, sim.simx_opmode_blocking)


def get_utilities(rec_client_id):
    global maze_array_4, maze_array_1, maze_array_2, maze_array_3, revolute_handle_yz_t4, revolute_handle_xz_t4, revolute_handle_yz_t1, revolute_handle_xz_t1, filename, t4_handle, t1_handle, t2_handle, t3_handle
    global revolute_handle_yz_t2, revolute_handle_xz_t2, revolute_handle_yz_t3, revolute_handle_xz_t3, vision_sensor_handle_4, vision_sensor_handle_3, vision_sensor_handle_2, vision_sensor_handle_1, vision_sensor_handle_5, data
    filename = "ball_details.json"
    img_file_path_4 = 'maze_t4'+'.jpg'
    img_file_path_1 = 'maze_t1'+'.jpg'
    img_file_path_2 = 'maze_t2'+'.jpg'
    img_file_path_3 = 'maze_t3'+'.jpg'
    input_img_4 = cv2.imread(img_file_path_4)
    input_img_1 = cv2.imread(img_file_path_1)
    input_img_2 = cv2.imread(img_file_path_2)
    input_img_3 = cv2.imread(img_file_path_3)
    warped_img_4 = task_1b.applyPerspectiveTransform(input_img_4)
    maze_array_4 = task_1b.detectMaze(warped_img_4)
    warped_img_1 = task_1b.applyPerspectiveTransform(input_img_1)
    maze_array_1 = task_1b.detectMaze(warped_img_1)
    warped_img_2 = task_1b.applyPerspectiveTransform(input_img_2)
    maze_array_2 = task_1b.detectMaze(warped_img_2)
    warped_img_3 = task_1b.applyPerspectiveTransform(input_img_3)
    maze_array_3 = task_1b.detectMaze(warped_img_3)
    return_code = task_2b.send_data(
        rec_client_id, maze_array_4, maze_array_1, maze_array_2, maze_array_3)
    return_code = task_2a.start_simulation(rec_client_id)
    print("Simulation started successfully")
    return_code, revolute_handle_yz_t4 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t4_1', sim.simx_opmode_blocking)
    return_code, revolute_handle_xz_t4 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t4_2', sim.simx_opmode_blocking)
    return_code, revolute_handle_xz_t1 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t1_2', sim.simx_opmode_blocking)
    return_code, revolute_handle_yz_t1 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t1_1', sim.simx_opmode_blocking)
    return_code, revolute_handle_xz_t2 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t2_2', sim.simx_opmode_blocking)
    return_code, revolute_handle_yz_t2 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t2_1', sim.simx_opmode_blocking)
    return_code, revolute_handle_xz_t3 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t3_2', sim.simx_opmode_blocking)
    return_code, revolute_handle_yz_t3 = sim.simxGetObjectHandle(
        rec_client_id, 'revolute_joint_ss_t3_1', sim.simx_opmode_blocking)

    return_code, vision_sensor_handle_5 = sim.simxGetObjectHandle(
        rec_client_id, 'vision_sensor_5', sim.simx_opmode_blocking)
    return_code, vision_sensor_handle_4 = sim.simxGetObjectHandle(
        rec_client_id, 'vision_sensor_4', sim.simx_opmode_blocking)
    return_code, vision_sensor_handle_1 = sim.simxGetObjectHandle(
        rec_client_id, 'vision_sensor_1', sim.simx_opmode_blocking)
    return_code, vision_sensor_handle_2 = sim.simxGetObjectHandle(
        rec_client_id, 'vision_sensor_2', sim.simx_opmode_blocking)
    return_code, vision_sensor_handle_3 = sim.simxGetObjectHandle(
        rec_client_id, 'vision_sensor_3', sim.simx_opmode_blocking)

    return_code, t4_handle = sim.simxGetObjectHandle(
        rec_client_id, 'pegs_t4_1', sim.simx_opmode_blocking)
    return_code, t1_handle = sim.simxGetObjectHandle(
        rec_client_id, 'pegs_t1_1', sim.simx_opmode_blocking)
    return_code, t2_handle = sim.simxGetObjectHandle(
        rec_client_id, 'pegs_t2_1', sim.simx_opmode_blocking)
    return_code, t3_handle = sim.simxGetObjectHandle(
        rec_client_id, 'pegs_t3_1', sim.simx_opmode_blocking)
    f = open(filename)
    data = json.load(f)


def find_pixel_path(rec_client_id, color):
    global maze_array_4, maze_array_1, maze_array_2, maze_array_3, revolute_handle_yz_t4, revolute_handle_xz_t4, revolute_handle_yz_t1, revolute_handle_xz_t1, revolute_handle_yz_t2, revolute_handle_xz_t2, revolute_handle_yz_t3, revolute_handle_xz_t3, vision_sensor_handle_4, vision_sensor_handle_1, vision_sensor_handle_2, vision_sensor_handle_3, data
    global t4_handle, t3_handle, t2_handle, t1_handle, dic
    dic = {
        "T1_CB1": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (5, 9),
            "start_cord_table_B": (5, 0),
            "end_cord_table_B": (0, 4),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_1,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t1,
            "revolute_handle_yz_B": revolute_handle_yz_t1,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_1,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_yz_t1,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_xz_t1,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t1_1',
            "tA_handle": t4_handle,
            "tB_handle": t1_handle,
            "angle_A": -60,
            "angle_B": -90,
            "removal_point_A": (1216, 704),
            "append_point_A": (1310, 704),
            "removal_point_B": (576, 64),
            "append_point_B": (576, 10)

        },
        "T1_CB2": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (5, 9),
            "start_cord_table_B": (5, 0),
            "end_cord_table_B": (4, 9),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_1,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t1,
            "revolute_handle_yz_B": revolute_handle_yz_t1,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_1,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_xz_t1,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_yz_t1,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t1_1',
            "tA_handle": t4_handle,
            "tB_handle": t1_handle,
            "angle_A": -60,
            "angle_B": -90,
            "removal_point_A": (1216, 704),
            "append_point_A": (1310, 704),
            "removal_point_B": (1216, 576),
            "append_point_B": (1310, 576)
        },
        "T1_CB3": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (5, 9),
            "start_cord_table_B": (5, 0),
            "end_cord_table_B": (9, 5),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_1,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t1,
            "revolute_handle_yz_B": revolute_handle_yz_t1,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_1,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_yz_t1,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_xz_t1,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t1_1',
            "tA_handle": t4_handle,
            "tB_handle": t1_handle,
            "angle_A": -60,
            "angle_B": 90,
            "removal_point_A": (1216, 704),
            "append_point_A": (1310, 704),
            "removal_point_B": (704, 1216),
            "append_point_B": (704, 1310)



        },
        "T2_CB1": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (9, 4),
            "start_cord_table_B": (0, 4),
            "end_cord_table_B": (4, 9),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_2,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t2,
            "revolute_handle_yz_B": revolute_handle_yz_t2,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_2,
            "excess_handle_A": revolute_handle_yz_t4,
            "excess_handle_B": revolute_handle_xz_t2,
            "less_handle_A": revolute_handle_xz_t4,
            "less_handle_B": revolute_handle_yz_t2,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t2_1',
            "tA_handle": t4_handle,
            "tB_handle": t2_handle,
            "angle_A": 60,
            "angle_B": -90,
            "removal_point_A": (576, 1216),
            "append_point_A": (576, 1216),
            "removal_point_B": (1216, 576),
            "append_point_B": (1310, 576)


        },
        "T2_CB2": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (9, 4),
            "start_cord_table_B": (0, 4),
            "end_cord_table_B": (9, 5),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_2,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t2,
            "revolute_handle_yz_B": revolute_handle_yz_t2,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_2,
            "excess_handle_A": revolute_handle_yz_t4,
            "excess_handle_B": revolute_handle_yz_t2,
            "less_handle_A": revolute_handle_xz_t4,
            "less_handle_B": revolute_handle_xz_t2,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t2_1',
            "tA_handle": t4_handle,
            "tB_handle": t2_handle,
            "angle_A": 60,
            "angle_B": 90,
            "removal_point_A": (576, 1216),
            "append_point_A": (576, 1310),
            "removal_point_B": (704, 1216),
            "append_point_B": (704, 1310)


        },
        "T2_CB3": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (9, 4),
            "start_cord_table_B": (0, 4),
            "end_cord_table_B": (5, 0),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_2,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t2,
            "revolute_handle_yz_B": revolute_handle_yz_t2,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_2,
            "excess_handle_A": revolute_handle_yz_t4,
            "excess_handle_B": revolute_handle_xz_t2,
            "less_handle_A": revolute_handle_xz_t4,
            "less_handle_B": revolute_handle_yz_t2,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t2_1',
            "tA_handle": t4_handle,
            "tB_handle": t2_handle,
            "angle_A": 60,
            "angle_B": 90,
            "removal_point_A": (576, 1216),
            "append_point_A": (576, 1310),
            "removal_point_B": (64, 704),
            "append_point_B": (10, 704)


        },
        "T3_CB1": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (4, 0),
            "start_cord_table_B": (4, 9),
            "end_cord_table_B": (9, 5),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_3,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t3,
            "revolute_handle_yz_B": revolute_handle_yz_t3,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_3,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_yz_t3,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_xz_t3,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t3_1',
            "tA_handle": t4_handle,
            "tB_handle": t3_handle,
            "angle_A": 60,
            "angle_B": 90,
            "removal_point_A": (64, 576),
            "append_point_A": (64, 576),
            "removal_point_B": (704, 1216),
            "append_point_B": (704, 1310)


        },
        "T3_CB2": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (4, 0),
            "start_cord_table_B": (4, 9),
            "end_cord_table_B": (5, 0),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_3,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t3,
            "revolute_handle_yz_B": revolute_handle_yz_t3,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_3,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_xz_t3,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_yz_t3,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t3_1',
            "tA_handle": t4_handle,
            "tB_handle": t3_handle,
            "angle_A": 60,
            "angle_B": 90,
            "removal_point_A": (64, 576),
            "append_point_A": (64, 576),
            "removal_point_B": (64, 704),
            "append_point_B": (10, 704)


        },
        "T3_CB3": {
            "start_cord_table_A": (0, 5),
            "end_cord_table_A": (4, 0),
            "start_cord_table_B": (4, 9),
            "end_cord_table_B": (0, 4),
            "maze_array_A": maze_array_4,
            "maze_array_B": maze_array_3,
            "revolute_handle_xz_A": revolute_handle_xz_t4,
            "revolute_handle_yz_A": revolute_handle_yz_t4,
            "revolute_handle_xz_B": revolute_handle_xz_t3,
            "revolute_handle_yz_B": revolute_handle_yz_t3,
            "vision_sensor_handle_A": vision_sensor_handle_4,
            "vision_sensor_handle_B": vision_sensor_handle_3,
            "excess_handle_A": revolute_handle_xz_t4,
            "excess_handle_B": revolute_handle_yz_t3,
            "less_handle_A": revolute_handle_yz_t4,
            "less_handle_B": revolute_handle_xz_t3,
            "table_name_A": 'top_plate_respondable_t4_1',
            "table_name_B": 'top_plate_respondable_t3_1',
            "tA_handle": t4_handle,
            "tB_handle": t3_handle,
            "angle_A": 60,
            "angle_B": -90,
            "removal_point_A": (64, 576),
            "append_point_A": (64, 565),
            "removal_point_B": (576, 64),
            "append_point_B": (576, 10)


        },



    }

    des = data[color][0]
    print(des)
    send_color_and_collection_box_identified(color, des)
    data[color].pop(0)
    start_cord_table_A = dic[des]["start_cord_table_A"]
    end_cord_table_A = dic[des]["end_cord_table_A"]
    start_cord_table_B = dic[des]["start_cord_table_B"]
    end_cord_table_B = dic[des]["end_cord_table_B"]
    maze_array_A = dic[des]["maze_array_A"]
    maze_array_B = dic[des]["maze_array_B"]
    path_A = return_path(maze_array_A, start_cord_table_A, end_cord_table_A)
    path_B = return_path(maze_array_B, start_cord_table_B, end_cord_table_B)
    pixel_path_A = task_4b.convert_path_to_pixels(path_A)
    pixel_path_B = task_4b.convert_path_to_pixels(path_B)
    pixel_path_A = remove_setpoints(pixel_path_A)
    pixel_path_A.remove(dic[des]["removal_point_A"])
    pixel_path_A.append(dic[des]["append_point_A"])
    pixel_path_B = remove_setpoints(pixel_path_B)
    pixel_path_B.remove(dic[des]["removal_point_B"])
    pixel_path_B.append(dic[des]["append_point_B"])
    revolute_handle_xz_A = dic[des]["revolute_handle_xz_A"]
    revolute_handle_yz_A = dic[des]["revolute_handle_yz_A"]
    revolute_handle_xz_B = dic[des]["revolute_handle_xz_B"]
    revolute_handle_yz_B = dic[des]["revolute_handle_yz_B"]
    vision_sensor_handle_A = dic[des]["vision_sensor_handle_A"]
    vision_sensor_handle_B = dic[des]["vision_sensor_handle_B"]
    angle_A = dic[des]["angle_A"]
    angle_B = dic[des]["angle_B"]
    excess_handle_A = dic[des]["excess_handle_A"]
    excess_handle_B = dic[des]["excess_handle_B"]
    less_handle_A = dic[des]["less_handle_A"]
    less_handle_B = dic[des]["less_handle_B"]
    table_name_A = dic[des]["table_name_A"]
    table_name_B = dic[des]["table_name_B"]
    tA_handle = dic[des]["tA_handle"]
    tB_handle = dic[des]["tB_handle"]

    return path_A, path_B, pixel_path_A, pixel_path_B, revolute_handle_xz_A, revolute_handle_yz_A, revolute_handle_xz_B, revolute_handle_yz_B, vision_sensor_handle_A, vision_sensor_handle_B, angle_A, angle_B, excess_handle_A, excess_handle_B, table_name_A, table_name_B, less_handle_A, less_handle_B, tA_handle, tB_handle


def when_to_start(img):
    objcorner = 0
    _, thresh = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY)
    contours, heirarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        objcorner = len(approx)
    return objcorner


def find_color(img):
    color = ''
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_grey, 25, 255, cv2.THRESH_BINARY)
    contours, heirarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        objcorner = len(approx)
        if objcorner >= 8:
            M = cv2.moments(cnt)
            Cx = int(M["m10"] / M["m00"])
            Cy = int(M["m01"] / M["m00"])
            b, g, r = img[Cy, Cx]
            if ((b > 110) or (b == 255)):
                color = 'blue'

            elif ((g > 110) or (g == 255)):
                color = 'green'

            elif ((r > 110) or (r == 255)):
                color = 'red'

    return color


def remove_setpoints(ls):
    l = []

    for i in range(1, len(ls)-1):

        x = ls[i][0]
        y = ls[i][1]
        x1 = ls[i-1][0]
        y1 = ls[i-1][1]
        x2 = ls[i+1][0]
        y2 = ls[i+1][1]
        prediffx = abs((x-x1))
        prediffy = abs((y-y1))
        postdiffx = abs((x-x2))
        postdiffy = abs((y-y2))
        if(abs(prediffx-postdiffx) == 0 or abs(prediffy-postdiffy) == 0):
            pass
        else:
            l.append(ls[i])
    l.append(ls[-1])
    return l


def run_every_time(rec_client_id):
    global vision_sensor_handle_5
    color = 0
    while(True):
        vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(
            rec_client_id, vision_sensor_handle_5)
        transformed_image = task_2a.transform_vision_sensor_image(
            vision_sensor_image, image_resolution)

        if(when_to_start(transformed_image) > 8):
            vision_sensor_image, image_resolution, return_code = task_2b.get_vision_sensor_image(
                rec_client_id, vision_sensor_handle_5)
            transformed_image_color = task_2b.transform_vision_sensor_image(
                vision_sensor_image, image_resolution)
            color = find_color(transformed_image_color)
            break
    return color


def get_starting_centroids(rec_client_id, vision_sensor_handle):
    center_x = 0
    center_y = 0
    while(True):
        vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(
            rec_client_id, vision_sensor_handle)
        transformed_image = task_2a.transform_vision_sensor_image(
            vision_sensor_image, image_resolution)
        warped_img = task_1b.applyPerspectiveTransform_2(
            transformed_image)
        shapes = when_to_rotate(warped_img)
        if(shapes != {}):
            center_x = shapes['Circle'][1]
            center_y = shapes['Circle'][2]
            break
    return center_x, center_y


def when_to_rotate(img_grey):
    
    lst = []
    shapes = {}
    objcorner = 0
    tt = img_grey > 83
    tt_1 = img_grey < 86
    tt_3 = tt & tt_1
    tt_4 = np.invert(tt_3)
    img_grey[tt_4] = 0
    contours, heirarchy = cv2.findContours(
        img_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
        objcorner = len(approx)

        if objcorner >= 9:
            M = cv2.moments(cnt)
            Cx = int(M["m10"] / M["m00"])
            Cy = int(M["m01"] / M["m00"])

            shape = "Circle"
            lst.append(None)
            lst.append(Cx)
            lst.append(Cy)
            shapes[shape] = lst
           

    return shapes


def rotate_extra(rec_client_id, excess_handle, angle, less_handle):
    a = 0
    while(a != 50000):
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, excess_handle, ((angle*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, less_handle, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        a += 1


def return_path(maze_array, start_coord, end_coord):
    path = task_4a.find_path(maze_array, start_coord, end_coord)
    return path


def delete_path(rec_client_id, table_name):
    inputBuffer = bytearray()

    return_code, retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,
                                                                                        table_name, sim.sim_scripttype_customizationscript, 'deletePath', [],
                                                                                        [], [], inputBuffer, sim.simx_opmode_blocking)


def make_stable(rec_client_id, excess_handle, less_handle):
    global revolute_handle_yz_t4, revolute_handle_xz_t4
    a = 0
    while(a != 25000):
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_yz_t4, ((-20*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_xz_t4, ((-20*np.pi)/180), sim.simx_opmode_oneshot)
        a += 1


def traversal(rec_client_id, path_A, path_B, pixel_path_A, pixel_path_B, revolute_handle_xz_A, revolute_handle_yz_A, revolute_handle_xz_B, revolute_handle_yz_B, vision_sensor_handle_A, vision_sensor_handle_B, angle_A, angle_B, excess_handle_A, excess_handle_B, table_name_A, table_name_B, less_handle_A, less_handle_B, tA_handle, tB_handle):
    task_4b.send_data_to_draw_path(rec_client_id, path_A, table_name_A)

    invert_model_properties(tA_handle)
    # time.sleep(1.3)

    center_x, center_y = get_starting_centroids(
        rec_client_id, vision_sensor_handle_A)
    # make_stable(rec_client_id, excess_handle_A, less_handle_A)
    print("Traversing ball on table A")
    if table_name_B=="top_plate_respondable_t1_1":
        task_4b.traverse_path(rec_client_id, pixel_path_A, revolute_handle_xz_A,
                          revolute_handle_yz_A, vision_sensor_handle_A, center_x, center_y, 2.9, 0.0038, 4.74)
    elif table_name_B=="top_plate_respondable_t2_1":
        task_4b.traverse_path(rec_client_id, pixel_path_A, revolute_handle_xz_A,
                          revolute_handle_yz_A, vision_sensor_handle_A, center_x, center_y, 2.9, 0.0045, 4.74)
        
    else:
        task_4b.traverse_path(rec_client_id, pixel_path_A, revolute_handle_xz_A,
                          revolute_handle_yz_A, vision_sensor_handle_A, center_x, center_y, 2.9, 0.0038, 4.74)
    
    
    task_3.errsum_x = 0
    task_3.errsum_y = 0
    task_3.lasterr_x =0
    task_3.lasterr_y =0

    rotate_extra(rec_client_id, excess_handle_A, angle_A, less_handle_A)
    delete_path(rec_client_id, table_name_A)
    invert_model_properties(tA_handle)
    task_4b.send_data_to_draw_path(rec_client_id, path_B, table_name_B)
    invert_model_properties(tB_handle)
    # time.sleep(2.0)
    center_x, center_y = get_starting_centroids(
        rec_client_id, vision_sensor_handle_B)
    print("Traversing ball on table B")
    if(table_name_B=="top_plate_respondable_t1_1"):
        task_4b.traverse_path(rec_client_id, pixel_path_B, revolute_handle_xz_B,
                          revolute_handle_yz_B, vision_sensor_handle_B, center_x, center_y, 2.9, 0.0025, 5.0)
    elif(table_name_B=="top_plate_respondable_t2_1"):
        task_4b.traverse_path(rec_client_id, pixel_path_B, revolute_handle_xz_B,
                          revolute_handle_yz_B, vision_sensor_handle_B, center_x, center_y, 2.82, 0.002, 5.28)
    else:
        task_4b.traverse_path(rec_client_id, pixel_path_B, revolute_handle_xz_B,
                          revolute_handle_yz_B, vision_sensor_handle_B, center_x, center_y, 2.87, 0.002, 5.2)
      


   
    task_3.errsum_x = 0
    task_3.errsum_y = 0
    task_3.lasterr_x =0
    task_3.lasterr_y =0
    rotate_extra(rec_client_id, excess_handle_B, angle_B, less_handle_B)

    delete_path(rec_client_id, table_name_B)
    invert_model_properties(tB_handle)

##############################################################


def main(rec_client_id):
    """
    Purpose:
    ---

    Teams are free to design their code in this task.
    The test executable will only call this function of task_5.py.
    init_remote_api_server() and exit_remote_api_server() functions are already defined
    in the executable and hence should not be called by the teams.
    The obtained client_id is passed to this function so that teams can use it in their code.

    However NOTE:
    Teams will have to call start_simulation() and stop_simulation() function on their own.

    Input Arguments:
    ---
    `rec_client_id` 	:  integer
            client_id returned after calling init_remote_api_server() function from the executable.

    Returns:
    ---
    None

    Example call:
    ---
    main(rec_client_id)

    """
    ##############	ADD YOUR CODE HERE	##############

    global client_id, maze_array_4, maze_array_1, maze_array_2, maze_array_3, filename, vision_sensor_handle_5, t4_handle, t3_handle, t2_handle, t1_handle
    global revolute_handle_xz_t3, revolute_handle_yz_t3, revolute_handle_xz_t2, revolute_handle_yz_t2, revolute_handle_yz_t1, revolute_handle_xz_t1,revolute_handle_xz_t4, revolute_handle_yz_t4
    client_id = rec_client_id
    get_utilities(rec_client_id)
    invert_model_properties(t1_handle)
    invert_model_properties(t2_handle)
    invert_model_properties(t3_handle)
    invert_model_properties(t4_handle)

    for i in range(5):
        
        color = run_every_time(rec_client_id)

        path_A, path_B, pixel_path_A, pixel_path_B, revolute_handle_xz_A, revolute_handle_yz_A, revolute_handle_xz_B, revolute_handle_yz_B, vision_sensor_handle_A, vision_sensor_handle_B, angle_A, angle_B, excess_handle_A, excess_handle_B, table_name_A, table_name_B, less_handle_A, less_handle_B, tA_handle, tB_handle = find_pixel_path(
            rec_client_id, color)

        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_xz_t4, ((-60*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_yz_t4, ((30*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_xz_t1, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_yz_t1, ((-60*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_xz_t2, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_yz_t2, ((60*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_xz_t3, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        retr_2 = sim.simxSetJointTargetPosition(
            rec_client_id, revolute_handle_yz_t3, ((60*np.pi)/180), sim.simx_opmode_oneshot)
        # time.sleep(2)
        traversal(rec_client_id, path_A, path_B, pixel_path_A, pixel_path_B, revolute_handle_xz_A, revolute_handle_yz_A, revolute_handle_xz_B, revolute_handle_yz_B,
                  vision_sensor_handle_A, vision_sensor_handle_B, angle_A, angle_B, excess_handle_A, excess_handle_B, table_name_A, table_name_B, less_handle_A, less_handle_B, tA_handle, tB_handle)

        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_xz_A, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_yz_A, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_xz_B, ((0*np.pi)/180), sim.simx_opmode_oneshot)
        # retr_2 = sim.simxSetJointTargetPosition(
        #     rec_client_id, revolute_handle_yz_B, ((0*np.pi)/180), sim.simx_opmode_oneshot)

    time.sleep(2)
    # task_2a.stop_simulation(rec_client_id)
    ##################################################


# Function Name:    main (built in)
#        Inputs:    None
#       Outputs:    None
#       Purpose:    To call the main(rec_client_id) function written by teams when they
#					run task_5.py only.
# NOTE: Write your solution ONLY in the space provided in the above functions. This function should not be edited.
if __name__ == "__main__":

    client_id = task_2a.init_remote_api_server()
    main(client_id)
