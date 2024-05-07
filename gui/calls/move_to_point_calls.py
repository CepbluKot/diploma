from threading import Thread
from time import sleep
from tkinter.ttk import  Treeview
from typing import Dict
from gui.output import axis_set_angle_slider_data
from servo_realization.output import control_algorithms, robot


def move_to_point_call():
    target_angles: Dict[int, int] = {}
    for axis_id in axis_set_angle_slider_data:
        target_angles[axis_id] = axis_set_angle_slider_data[axis_id]()

    control_algorithms.move_to_point(max_speed=robot.speed, target_angles=target_angles)


def move_multiple_points(tree: Treeview):
    def move_multiple_points_for_thread():
        current_target_positions: Dict[int, int] = {}
        # gui animation
        prev_row = None

        for row_with_point_data in tree.get_children():
            curr_row = tree.item(row_with_point_data)
            if prev_row:
                prev_row_tag = prev_row['tags'][0]
                tree.tag_configure(prev_row_tag, background='white')

            curr_row_tag = curr_row['tags'][0]
            tree.tag_configure(curr_row_tag, background='blue')


            # get target angles data
            curr_row_vals = curr_row['values']

            axis_id = 1
            for axis_target_angle_val in curr_row_vals:
                if axis_target_angle_val == 'None':
                    current_target_positions[axis_id] = -1

                else:
                    pulses_per_rev = robot.servos[axis_id].pulses_per_revolution
                    gearbox_val = robot.servos[axis_id].gearbox_value
                    current_target_positions[axis_id] = pulses_per_rev*gearbox_val/360*float(axis_target_angle_val)
                
                axis_id += 1
 
            # send command to robot
            
            control_algorithms.move_to_point(max_speed=robot.speed, target_angles=current_target_positions)
            sleep(6)

        if prev_row:
            prev_row_tag = prev_row['tags'][0]
            tree.tag_configure(prev_row_tag, background='white')

    move_multiple_points_thr = Thread(target=move_multiple_points_for_thread)
    move_multiple_points_thr.start()
