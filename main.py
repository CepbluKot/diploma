import datetime
from gui.output import init_gui
# from gui.calls.set_params_calls import *
# from gui.calls.move_to_point_calls import *
import multiprocessing
from x import run

p1 = multiprocessing.Process(target=init_gui)
p2 = multiprocessing.Process(target=run)
p2.start()
p1.start()
p1.join()
p2.join()

# init_gui()
# # run()