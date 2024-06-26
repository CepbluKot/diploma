import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


last_msg = []


def on_new_data(data):
    global last_msg
    last_msg = pickle.loads(data)


def update_line(num, iterator, line):
    scan = last_msg

    if scan:
        offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
        line.set_offsets(offsets)
        intens = np.array([meas[0] for meas in scan])
        line.set_array(intens)
    return line

DMAX = 4000
IMIN = 0
IMAX = 50

def run():
    fig = plt.figure()
    fig.canvas.manager.set_window_title("LiDar")
    ax = plt.subplot(111, projection="polar")
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    iterator=None
    ani = animation.FuncAnimation(fig, update_line,
        fargs=( iterator, line), interval=50)
    
    plt.show()
