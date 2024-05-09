from tkinter import *
from tkinter.ttk import Combobox
import tkintermapview


def map_tab(frame):
    map_widget = tkintermapview.TkinterMapView(frame, width=500, height=50, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

    # set current position and zoom
    map_widget.set_position(56.285759, 38.739335, marker=True)  # Berlin, Germany
    
    map_widget.set_position(1,1,marker=True)
    # frame.mainloop()
