import typing
from tkinter.ttk import Frame, Notebook, Treeview
from tkinter import *

from gui.controls_tab.controls_tab import controls_tab
from gui.connection_config_tab.connection_config_tab import connection_config_tab
from gui.depth_cam_tab.depth_cam_tab import depths_cam_tab
# from gui.lidar_tab.lidar_tab import lidar_tab

axis_set_angle_slider_data = {}

def init_gui():
    window = Tk()
    window.title("Robot service app")
    window.geometry('1500x900')
    
    tab_control = Notebook(window)  
    tab1 = Frame(tab_control)  
    tab2 = Frame(tab_control)
    tab3 = Frame(tab_control)
    tab4 = Frame(tab_control)
    
    tab_control.add(tab1, text='controls_tab')  
    tab_control.add(tab2, text='connection_config')
    tab_control.add(tab3, text='depth_cam')  
    tab_control.add(tab4, text='lidar')  
    tab_control.pack(expand=1, fill='both')  

    
    controls_tab(tab1)
    connection_config_tab(tab2)
    depths_cam_tab(tab3)
    # lidar_tab(tab4)

    
    window.mainloop()
