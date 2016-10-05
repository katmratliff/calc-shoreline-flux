#!/usr/bin/python

import numpy as np
import pudb


""" Parameters """

no_angles = 181      # how many angles to use
lower_bound = -90     # lowest angle to test
upper_bound = 90    # highest angle to test

timestep = 1 		# days

# wave & coastline parameters
Asymmetry = .5		# A, fraction of waves approaching from left
Highness = .5		# u, fraction of waves approaching from high angles

OffShoreWvHt = 1    	# offhsore wave height (m)
Period = 10      		# offshore wave period (s)
DepthShoreface = 10 	# depth of shoreface (m)
cellwidth = 100 		# cell width for volume calculations (m)

np.random.seed(1234)


""" Determine which angles to test. """
angles_deg = np.linspace(lower_bound, upper_bound, num=no_angles)
angles = np.deg2rad(angles)

QsNet = np.zeroslike(angles)

""" Begin time loop. """

""" Calculate wave angle for current timestep. """

WaveAngle = WavesNextAngle(Asymmetry,Highness)


""" Loop through angles to determine sediment transport. """
for i in xrange(len(angles)):

	AngleDeep = WaveAngle - angles[i]

	if (AngleDeep > np.pi/2.0) or (AngleDeep < -np.pi/2.0):
		Qs = 0
	else:
		Qs = DetermineTransport(AngleDeep,OffShoreWvHt,Period
								DepthShoreface,cellwidth,timestep)
	if AngleDeep > 0:
		QsNet[i] += Qs
	else:
		QsNet[i] -= Qs


def DetermineTransport(AngleDeep,OffShoreWvHt,Period,DepthShoreface,cellwidth,timestep):

	# coefficients
	StartDepth = 3 * OffShoreWvHt	# m, depth to begin refraction calcs (beyond breakers)
	RefractStep = 0.2				# m, step size to iterate depth for refraction calcs
	KBreak = 0.5					# coefficient for wave breaking threshold

	# important constants
	g = 9.80665 		# gravitational acceleration (m/s^2)
	rho = 1020			# kg/m^3, density of water + dissolved matter

	# calculate deep water celerity & length, Komar 5.11
	CDeep = g * Period / (2.0 * np.pi)
	LDeep = CDeep * Period

	Depth = StartDepth	# water depth for current iteration

	refracting = True
	while refracting: 

		# non-iterative eqn for L, from Fenton & McKee
		WaveLength = LDeep * (np.tanh((((2.0*np.pi/Period)^2) * (Depth/g))^(3/4)))^(2/3)

		C = WaveLength / Period

		kh = np.pi * Depth / WaveLength

		# from Komar 5.21
		# NOTE: CHECK - COMMENTS IN CEM DON'T MATCH CODE
		n = 0.5 * (1 + 2.0 * kh / np.sinh(2.0 * kh))

		# calculate angle, assuming shore parallel contours and no conv/div or rays
		# from Komar 5.47
		Angle = np.arcsin(C / CDeep * np.sin(AngleDeep))

		# determine wave height from refract calcs - Komar 5.49
		WvHeight = OffShoreWvHt * (CDeep*np.cos(AngleDeep) / (C*2.0*n*np.cos(Angle)))^(1/2)

		if (WvHeight > (Depth * KBreak)) or (Depth <= RefractStep):
			refracting = False
			break
		else:
			Depth -= RefractStep

	# calculate volume transported
	VolumeTrans = np.absolute(1.1 * rho * (g^(3/2)) * (WvHeight^(12/5)) * \
				  np.cos(Angle) * np.sin(Angle) * timestep)

	# adjust volume to a flux
	VolAdjust = 1.0/cellwidth/cellwidth/DepthShoreface
	vv = VolumeTrans * VolAdjust

	return vv

def WavesNextAngle(Asymmetry,Highness):

	f = np.random.rand()

	if (f > Highness):
		angle = (f - Highness) / (1. - Highness) * np.pi * 0.25
	else:
		angle = ((f / Highness) + 1.) * np.pi * 0.25

	if (np.random.rand() > Asymmetry):
		angle *= -1.

	return angle





