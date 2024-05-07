import typing
from tkinter import *
import tkinter.ttk as ttk
from  matplotlib import animation
import  matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import tkinter as tk
import numpy as np
import os


def depths_cam_tab(frame):
    fig = plt.Figure()

    x = np.arange(0, 2*np.pi, 0.01)        # x-array

    def animate(i):
        if os.path.exists("temp2.mp4"):
            os.remove('temp2.mp4')
        line.set_ydata(np.sin(x+i/10.0))  # update the data
        return line

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(column=0,row=1)

    ax = fig.add_subplot(111)
    line, = ax.plot(x, np.sin(x))
    anim = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)
    
    anim.save('temp2.mp4')
