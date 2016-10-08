#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

no_angles = 181      # how many angles to use
lower_bound = -180     # lowest angle to test
upper_bound = 180  # highest angle to test

angles_deg = np.linspace(upper_bound, lower_bound, num=no_angles)
angles = np.deg2rad(angles_deg)

QsNet_01 = np.loadtxt('U01/Qs_net.out');
QsNet_02 = np.loadtxt('U02/Qs_net.out');
QsNet_03 = np.loadtxt('U03/Qs_net.out');
QsNet_04 = np.loadtxt('U04/Qs_net.out');
QsNet_05 = np.loadtxt('U05/Qs_net.out');
QsNet_06 = np.loadtxt('U06/Qs_net.out');
QsNet_07 = np.loadtxt('U07/Qs_net.out');
QsNet_08 = np.loadtxt('U08/Qs_net.out');
QsNet_09 = np.loadtxt('U09/Qs_net.out');
QsPerDay_01 = QsNet_01/5000;
QsPerDay_02 = QsNet_02/5000;
QsPerDay_03 = QsNet_03/5000;
QsPerDay_04 = QsNet_04/5000;
QsPerDay_05 = QsNet_05/5000;
QsPerDay_06 = QsNet_06/5000;
QsPerDay_07 = QsNet_07/5000;
QsPerDay_08 = QsNet_08/5000;
QsPerDay_09 = QsNet_09/5000;

f = plt.figure()
U01, = plt.plot(angles_deg, QsPerDay_01, color=[0.8, 0.8, 1], linewidth=2)
U02, = plt.plot(angles_deg, QsPerDay_02, color=[0.7, 0.7, 1], linewidth=2)
U03, = plt.plot(angles_deg, QsPerDay_03, color=[0.6, 0.6, 1], linewidth=2)
U04, = plt.plot(angles_deg, QsPerDay_04, color=[0.5, 0.5, 1], linewidth=2)
U05, = plt.plot(angles_deg, QsPerDay_05, color=[0.4, 0.4, 1], linewidth=2)
U06, = plt.plot(angles_deg, QsPerDay_06, color=[0.3, 0.3, 1], linewidth=2)
U07, = plt.plot(angles_deg, QsPerDay_07, color=[0.2, 0.2, 1], linewidth=2)
U08, = plt.plot(angles_deg, QsPerDay_08, color=[0.1, 0.1, 1], linewidth=2)
U09, = plt.plot(angles_deg, QsPerDay_09, color=[0, 0, 1], linewidth=2)
plt.legend((U01, U02, U03, U04, U05, U06, U07, U08, U09,),
		   ('U = 0.1', 'U = 0.2', 'U = 0.3', 'U = 0.4', 
		   'U = 0.5', 'U = 0.6', 'U = 0.7', 'U = 0.8',
		   'U = 0.9'), fontsize=12, loc=('upper left'), ncol=2)
# plt.axis = [(180, -180, -0.06, 0.1)]
plt.xlim([180, -180])
plt.ylim([-0.06, 0.08])
plt.xlabel('shoreline angle')
plt.ylabel('Qs per day')
plt.title('normalized flux for a given wave climate and shoreline angle')
plt.savefig('daily-Qs.png')
plt.close
