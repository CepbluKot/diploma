from servo_realization.output import robot


def set_speed_call(value):
    robot.speed = float(value)

    print('speed set', robot.speed)
    robot.send_all_axis_speeds(float(value))
