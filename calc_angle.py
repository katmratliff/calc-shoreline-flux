#!/usr/bin/python

import numpy as np


def WavesNextAngle(Asymmetry,Highness):

	f = np.random.rand()

	if (f > Highness):
		angle = (f - Highness) / (1. - Highness) * np.pi * 0.25
	else:
		angle = ((f / Highness) + 1.) * np.pi * 0.25

	if (np.random.rand() > Asymmetry):
		angle *= -1.

	return angle





