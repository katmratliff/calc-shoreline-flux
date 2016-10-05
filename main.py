#!/usr/bin/python

import numpy as np
import calc_angle
import calc_trans
import pudb


""" Parameters """

no_angles = 181      # how many angles to use
lower_bound = -90     # lowest angle to test
upper_bound = 90    # highest angle to test

timestep = 1 		# days
time_max = 10		# days

# wave & coastline parameters
Asymmetry = .5		# A, fraction of waves approaching from left
Highness = .5		# u, fraction of waves approaching from high angles

OffShoreWvHt = 1    	# offhsore wave height (m)
Period = 10      		# offshore wave period (s)
DepthShoreface = 10 	# depth of shoreface (m)
cellwidth = 100 		# cell width for volume calculations (m)

np.random.seed(1234)

pu.db

""" Determine which angles to test. """
angles_deg = np.linspace(lower_bound, upper_bound, num=no_angles)
angles = np.deg2rad(angles_deg)

wave_angles = np.zeros(time_max)
QsNet = np.zeros_like(angles)

""" Begin time loop. """

for k in xrange(0, time_max, timestep):

	""" Calculate wave angle for current timestep. """

	WaveAngle = calc_angle.WavesNextAngle(Asymmetry,Highness)
	wave_angles[k] = np.rad2deg(WaveAngle)


	""" Loop through angles to determine sediment transport. """
	for i in xrange(len(angles)):

		AngleDeep = WaveAngle - angles[i]

		if (AngleDeep > np.pi/2.0) or (AngleDeep < -np.pi/2.0):
			Qs = 0
		else:
			Qs = calc_trans.DetermineTransport(AngleDeep,OffShoreWvHt,Period,
									DepthShoreface,cellwidth,timestep)
		if AngleDeep > 0:
			QsNet[i] += Qs
		else:
			QsNet[i] -= Qs

np.savetxt('angles_tested',angles_deg,'%.3f')
np.savetxt('wave_angles',wave_angles,'%.3f')
np.savetxt('Qs_net',QsNet,'%.5f')
