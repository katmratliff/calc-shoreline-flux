#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import calc_angle
import calc_trans


""" Parameters """

no_angles = 181      # how many angles to use
lower_bound = -180     # lowest angle to test
upper_bound = 180  # highest angle to test

timestep = 1 		# days
time_max = 5000		# days

# wave & coastline parameters
Asymmetry = .5		# A, fraction of waves approaching from left (0<A<1)
Highness = .2		# u, fraction of waves approaching from high angles (0<U<1)

OffShoreWvHt = 1    	# offhsore wave height (m)
Period = 10      		# offshore wave period (s)
DepthShoreface = 10 	# depth of shoreface (m)
cellwidth = 100 		# cell width for volume calculations (m)

np.random.seed(1234)

""" Determine which angles to test. """
angles_deg = np.linspace(upper_bound, lower_bound, num=no_angles)
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

max_loc_value = [angles_deg[np.argmax(QsNet)], np.amax(QsNet)]

f = plt.figure()
plt.hist(wave_angles, 30)
plt.title('wave angles')
plt.xlabel('angle')
plt.ylabel('frequency')
plt.savefig('binned_wave_angles.png')
plt.close(f)

p = plt.figure()
plt.plot(angles_deg, QsNet/time_max)
# plt.plot(np.argmax(QsNet), np.amax(QsNet), s=2)
plt.axis([upper_bound, lower_bound, np.amin(QsNet) - 0.1*np.fabs(np.amin(QsNet)),
		  np.amax(QsNet) + 0.1*np.amax(QsNet)])
plt.xlabel('shoreline angle')
plt.ylabel('Qs/day')
plt.savefig('qs_net_fig.png')
plt.close(p)

np.savetxt('angles_tested.out',angles_deg,'%.3f')
np.savetxt('wave_angles.out',wave_angles,'%.3f')
np.savetxt('Qs_net.out',QsNet,'%.5f')
np.savetxt('max_value.out',max_loc_value,'%.5f')