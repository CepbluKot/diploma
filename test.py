import tkinter, threading
import tkintermapview


root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

old_marker = None
def stuff():
    import random
    global old_marker
    old_marker.delete()
    
    old_marker=  map_widget.set_position(random.randint(40,50),random.randint(40,50),marker=True)
    root_tk.after(3000, stuff)

btn_move_forward_left_eng = tkinter.Button(master=root_tk, text="↑", command=stuff)
# btn_move_forward_left_eng.grid(row=2, column=1, padx=(100, 10), pady=10)
btn_move_forward_left_eng.pack()

map_widget = tkintermapview.TkinterMapView(root_tk, width=500, height=50, corner_radius=0)
map_widget.pack(fill="both", expand=True)

map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

# set current position and zoom
old_marker = map_widget.set_position(56.285759, 38.739335, marker=True)  # Berlin, Germany


root_tk.after(3000, stuff)

root_tk.mainloop()
