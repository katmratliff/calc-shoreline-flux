#!/usr/bin/python

import numpy as np


""" Parameters """

no_angles = 91      # how many angles to use
lower_bound = 0     # lowest angle to test
upper_bound = 90    # highest angle to test




angles = np.linspace(lower_bound, upper_bound, num=no_angles)
angles_rad = np.deg2rad(angles)