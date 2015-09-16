__author__ = 'unit978'


# Linear interpolation.
def lerp(start, end, time_step):

    return (1.0 - time_step) * start + time_step * end