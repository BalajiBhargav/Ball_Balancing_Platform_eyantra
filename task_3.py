'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 3 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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

# Team ID:          [544]
# Author List:      [Bhargav,Saketh,Jeevanandan,Sreekar]
# Filename:         task_3.py
# Functions:        init_setup(rec_client_id), control_logic(center_x,center_y), change_setpoint(new_setpoint)
#                   []
# Global variables: client_id, setpoint=[]
# 					[revolute_handle_yz,revolute_handle_xz,last_time,errsum_x,errsum_y,derr_x,derr_y,lasterr_x,lasterr_y,l]


####################### IMPORT MODULES #########################
## You are not allowed to make any changes in this section.   ##
## You have to implement this task with the six available     ##
## modules for this task (numpy,opencv,os,sys,traceback,time) ##
################################################################
import numpy as np
import cv2
import os
import sys
import traceback
import time

##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
    import sim

except Exception:
    print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
    print('\n[WARNING] Make sure to have following files in the directory:')
    print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
    sys.exit()


# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1

# Global list "setpoint" for storing target position of ball on the platform/top plate
# The zeroth element stores the x pixel and 1st element stores the y pixel
# NOTE: DO NOT change the value of this "setpoint" list
setpoint = [576, 192]

# Global variable "vision_sensor_handle" to store handle for Vision Sensor
# NOTE: DO NOT change the value of this "vision_sensor_handle" variable here
vision_sensor_handle = 0

# You can add your global variables here
##############################################################
revolute_handle_yz = 0
revolute_handle_xz = 0
last_time = 0
errsum_x = 0
errsum_y = 0
derr_x = 0
derr_y = 0
lasterr_x = 0
lasterr_y = 0
l = 0
thewriter_x = 0
thewriter_y = 0
k_c = 0


##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

# For converting one range values to other range(used for servo angles) we used formula from stackoverflow:https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
# This is the formula we used:   NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin


##############################################################


def control_logic(center_x, center_y, revolute_handle_xz, revolute_handle_yz, client, k_p, k_i, k_d):
    """
    Purpose:
    ---
    This function should implement the control logic to balance the ball at a particular setpoint on the table.

    The orientation of the top table should "ONLY" be controlled by the servo motor as we would expect in a
    practical scenario.

    Hence "ONLY" the shaft of the servo motor or in other words the revolute joint between servo and servo fin
    should have 'motor enabled' and 'control loop enabled option' checked. Refer documentation for further understanding of
    these options.

    This function should use the necessary Legacy Python Remote APIs to control the revolute joints.

    NOTE: In real life, a 180 degree servo motor can rotate between -90 to +90 degrees or -1.57 to 1.57 radians only.
              Hence the command to be sent to servo motor should be between this range only. When the top plate is parallel to
              base plate, the revolute joint between servo and servo fin should be at 0 degrees orientation. Refer documentation
              for further understanding.

    NOTE: Since the simulation is dynamic in nature there should not by any bottlenecks in this code due to which the
              processing may take a lot of time. As a result 'control_logic' function should be called in every iteration of
              the while loop. Use global variables instead of reinitialising the varibles used in this function.

    Input Arguments:
    ---
    `center_x` 	:  [ int ]
            the x centroid of the ball

    `center_y` 	:  [ int ]
            the y centroid of the ball

    Returns:
    ---
    None

    Example call:
    ---
    control_logic(center_x,center_y)

    """
    global setpoint, client_id, last_time, lasterr_x, lasterr_y, errsum_x, errsum_y, l, k_c, thewriter_x, thewriter_y

    ##############	ADD YOUR CODE HERE	##############
    # print(setpoint)
    client_id = client
    error_x = setpoint[0]-center_x
    error_y = setpoint[1]-center_y
    # print("centers", center_x, center_y)
    # print("errors", error_x, error_y)
    now = time.time()
    time_change = now-last_time
    if l == 0:
        time_change = 0.1
    else:
        time_change = now-last_time
    # k_c += time_change
    # thewriter_x = csv.writer(open('op_x.csv', 'a', newline=''))
    # thewriter_x.writerow([k_c, center_x, setpoint[0]])
    # thewriter_y = csv.writer(open('op_y.csv', 'a', newline=''))
    # thewriter_y.writerow([k_c, center_y, setpoint[1]])
  
   
    kp = k_p
    ki = k_i
    kd = k_d
    # error_x = error_x
    # error_y = error_y
    errsum_x += (error_x*time_change)
    errsum_y += (error_y*time_change)
    # print("errorsumx,errorumy",errsum_x,errsum_y);
    derr_x = (error_x-lasterr_x)/time_change
    derr_y = (error_y-lasterr_y)/time_change
    pid_p_x = kp*error_x
    pid_p_y = kp*error_y
    pid_d_x = kd*derr_x
    pid_d_y = kd*derr_y
    pid_i_x = ki*errsum_x
    pid_i_y = ki*errsum_y
    output_x = pid_d_x+pid_p_x
    output_y = pid_d_y+pid_p_y
    output_x += pid_i_x
    output_y += pid_i_y
    old_low_x = -640
    old_high_x = 640

    old_low_y = -640
    old_high_y = 640
    ran1 = old_high_y-old_low_y
    a = (output_x - (old_low_x))
    b = a*180
    ran = (old_high_x-old_low_x)
    c = b/ran
    NewValue_x = c - 90
    a1 = (output_y - (old_low_y))
    b1 = a1*180
    c1 = b1/ran1
    NewValue_y = (c1) - 90

    if NewValue_x < -90:
        NewValue_x = -90
    if NewValue_x > 90:
        NewValue_x = 90
    if NewValue_y < -90:
        NewValue_y = -90
    if NewValue_y > 90:
        NewValue_y = 90
    NewValue_x = round(NewValue_x, 2)
    NewValue_y = round(NewValue_y, 2)
    print("angles", -NewValue_x, NewValue_y)
    retr_1 = sim.simxSetJointTargetPosition(
        client_id, revolute_handle_yz, ((NewValue_y*np.pi)/180), sim.simx_opmode_oneshot)
    retr_2 = sim.simxSetJointTargetPosition(
        client_id, revolute_handle_xz, (-(NewValue_x*np.pi)/180), sim.simx_opmode_oneshot)
    lasterr_x = error_x
    lasterr_y = error_y
    last_time = now
    l += 1

    ##################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    change_setpoint
#        Inputs:    list of new setpoint-
#						new_setpoint=[x_pixel,y_pixel]
#       Outputs:    None
#       Purpose:    The function updates the value of global "setpoint" list after every 15 seconds of simulation time.
#					This will be ONLY called by executable file.
def change_setpoint(new_setpoint):

    global setpoint
    setpoint = new_setpoint[:]
    # errsum_x=0
    # errsum_y=0


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function does the following:
# 						- imports 'task_1b' file as module
# 						- imports 'task_1a_part1' file as module
#						- imports 'task_2a' file as module
# 						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
# 						- then calls start_simulation() function in 'task_2a' to start the simulation
#						- then calls init_setup() function to store the required handles in respective global variables and complete initializations if required
# 						- then calls get_vision_sensor_image() function in 'task_2a' to capture an image from the Vision Sensor in CoppeliaSim scene
# 						- If the return code is 'simx_return_ok':
# 									- then calls transform_vision_sensor_image() function in 'task_2a' to transform the captured image
# 						  			  to a format compatible with OpenCV.
#			 						- then the transformed image is given as input and Perspective Transform is applied
#			 						  by calling applyPerspectiveTransform function	from 'task_1b'
#			 						- then the output of warped_img is given to 'scan_image' function from 'task_1a_part1'
#			 			- then calls control_logic() function to command the servo motors

# NOTE: Write your solution ONLY in the space provided in the above functions. Main function should not be edited.
if __name__ == "__main__":

    # Import 'task_1b.py' file as module
    try:
        import task_1b

    except ImportError:
        print('\n[ERROR] task_1b.py file is not present in the current directory.')
        print('Your current directory is: ', os.getcwd())
        print('Make sure task_1b.py is present in this current directory.\n')
        sys.exit()

    except Exception as e:
        print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
        traceback.print_exc(file=sys.stdout)
        sys.exit()

    # Import 'task_1a_part1.py' file as module
    try:
        import task_1a_part1

    except ImportError:
        print(
            '\n[ERROR] task_1a_part1.py file is not present in the current directory.')
        print('Your current directory is: ', os.getcwd())
        print('Make sure task_1a_part1.py is present in this current directory.\n')
        sys.exit()

    except Exception as e:
        print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
        traceback.print_exc(file=sys.stdout)
        sys.exit()

    # Import 'task_2a.py' file as module
    try:
        import task_2a

    except ImportError:
        print('\n[ERROR] task_2a.py file is not present in the current directory.')
        print('Your current directory is: ', os.getcwd())
        print('Make sure task_2a.py is present in this current directory.\n')
        sys.exit()

    except Exception as e:
        print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
        traceback.print_exc(file=sys.stdout)
        sys.exit()

    # Initiate the Remote API connection with CoppeliaSim server
    print('\nConnection to CoppeliaSim Remote API Server initiated.')
    print('Trying to connect to Remote API Server...')

    try:
        client_id = task_2a.init_remote_api_server()

        if (client_id != -1):
            print('\nConnected successfully to Remote API Server in CoppeliaSim!')

            # Starting the Simulation
            try:
                return_code = task_2a.start_simulation()

                if (return_code == sim.simx_return_novalue_flag):
                    print('\nSimulation started correctly in CoppeliaSim.')

                    # Storing the required handles in respective global variables.
                    try:
                        init_setup(client_id)
                    except Exception:
                        print(
                            '\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
                        print(
                            'Stop the CoppeliaSim simulation manually if started.\n')
                        traceback.print_exc(file=sys.stdout)
                        print()
                        sys.exit()

                else:
                    print(
                        '\n[ERROR] Failed starting the simulation in CoppeliaSim!')
                    print(
                        'start_simulation function in task_2a.py is not configured correctly, check the code!')
                    print()
                    sys.exit()

            except Exception:
                print(
                    '\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
                print('Stop the CoppeliaSim simulation manually.\n')
                traceback.print_exc(file=sys.stdout)
                print()
                sys.exit()

        else:
            print('\n[ERROR] Failed connecting to Remote API server!')
            print('[WARNING] Make sure the CoppeliaSim software is running and')
            print(
                '[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
            print(
                '[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
            print()
            sys.exit()

    except Exception:
        print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
        print('Stop the CoppeliaSim simulation manually if started.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()

    # Initialising the center_x and center_y variable to the current position of the ball
    center_x = 1063
    center_y = 1063

    init_simulation_time = 0
    curr_simulation_time = 0

    # Storing time when the simulation started in variable init_simulation_time
    return_code_signal, init_simulation_time_string = sim.simxGetStringSignal(
        client_id, 'time', sim.simx_opmode_streaming)

    if(return_code_signal == 0):
        init_simulation_time = float(init_simulation_time_string)

    # Running the coppeliasim simulation for 15 seconds
    while(curr_simulation_time - init_simulation_time <= 15):

        return_code_signal, curr_simulation_time_string = sim.simxGetStringSignal(
            client_id, 'time', sim.simx_opmode_buffer)

        if(return_code_signal == 0):
            curr_simulation_time = float(curr_simulation_time_string)

        try:
            vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(
                vision_sensor_handle)

            if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
                # print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

                # Get the transformed vision sensor image captured in correct format
                try:
                    transformed_image = task_2a.transform_vision_sensor_image(
                        vision_sensor_image, image_resolution)

                    if (type(transformed_image) is np.ndarray):

                        # cv2.imshow('transformed image', transformed_image)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

                        # Get the resultant warped transformed vision sensor image after applying Perspective Transform
                        try:
                            warped_img = task_1b.applyPerspectiveTransform(
                                transformed_image)

                            if (type(warped_img) is np.ndarray):

                                # Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
                                try:
                                    shapes = task_1a_part1.scan_image(
                                        warped_img)

                                    if (type(shapes) is dict and shapes != {}):
                                        print(
                                            '\nShapes detected by Vision Sensor are: ')
                                        print(shapes)

                                        # Storing the detected x and y centroid in center_x and center_y variable repectively
                                        center_x = shapes['Circle'][1]
                                        center_y = shapes['Circle'][2]

                                    elif(type(shapes) is not dict):
                                        print('\n[ERROR] scan_image function returned a ' +
                                              str(type(shapes)) + ' instead of a dictionary.')
                                        print(
                                            'Stop the CoppeliaSim simulation manually.')
                                        print()
                                        sys.exit()

                                except Exception:
                                    print(
                                        '\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
                                    print(
                                        'Stop the CoppeliaSim simulation manually.\n')
                                    traceback.print_exc(file=sys.stdout)
                                    print()
                                    sys.exit()

                            else:
                                print(
                                    '\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
                                print('Stop the CoppeliaSim simulation manually.')
                                print()
                                sys.exit()

                        except Exception:
                            print(
                                '\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
                            print('Stop the CoppeliaSim simulation manually.\n')
                            traceback.print_exc(file=sys.stdout)
                            print()
                            sys.exit()

                    else:
                        print(
                            '\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
                        print('Stop the CoppeliaSim simulation manually.')
                        print()
                        sys.exit()

                except Exception:
                    print(
                        '\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
                    print('Stop the CoppeliaSim simulation manually.\n')
                    traceback.print_exc(file=sys.stdout)
                    print()
                    sys.exit()

            try:
                control_logic(center_x, center_y)

            except:
                print(
                    '\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
                print('Stop the CoppeliaSim simulation manually.\n')
                traceback.print_exc(file=sys.stdout)
                print()
                sys.exit()

        except Exception:
            print(
                '\n[ERROR] Your get_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
            print('Stop the CoppeliaSim simulation manually.\n')
            traceback.print_exc(file=sys.stdout)
            print()
            sys.exit()

    # Ending the Simulation
    try:
        return_code = task_2a.stop_simulation()

        if (return_code == sim.simx_return_novalue_flag):
            print('\nSimulation stopped correctly.')

            # Stop the Remote API connection with CoppeliaSim server
            try:
                task_2a.exit_remote_api_server()

                if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
                    print(
                        '\nDisconnected successfully from Remote API Server in CoppeliaSim!')

                else:
                    print(
                        '\n[ERROR] Failed disconnecting from Remote API server!')
                    print(
                        '[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

            except Exception:
                print(
                    '\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
                print('Stop the CoppeliaSim simulation manually.\n')
                traceback.print_exc(file=sys.stdout)
                print()
                sys.exit()

        else:
            print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
            print(
                '[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
            print('Stop the CoppeliaSim simulation manually.')

        print()
        sys.exit()

    except Exception:
        print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
        print('Stop the CoppeliaSim simulation manually.\n')
        traceback.print_exc(file=sys.stdout)
        print()
        sys.exit()
