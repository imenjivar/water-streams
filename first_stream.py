from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import math

G = 9.8  # acceleration due to gravity, in m/s^2
t_stop = 2  # how many seconds to simulate
stream_count = 10  # how many drops to shoot
x_lim = 7 # x axis limit
y_lim = 3 # y axis limit
initial_angle = math.radians(45) # initial angle in radians
initial_velocity = 8 # initial velocity

# create a time array from 0..t_stop sampled at 0.02 second steps
dt = 0.01
t = np.arange(0, t_stop, dt)

# function describing x position of a drop after t
def x_at(t):
    return initial_velocity*cos(initial_angle) * t

# function describing y positiopn of a drop after t
def y_at(t):
    return initial_velocity*sin(initial_angle) * t - (G * t * t)/2

# create graph
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(autoscale_on=False, xlim=(0, x_lim), ylim=(0, y_lim))
ax.set_aspect('equal')
ax.grid()

# calculate position of all the points at once
x = np.empty(len(t))
y = np.empty(len(t))
for i in range(1, len(t)):
    x[i] = x_at(t[i])
    y[i] = y_at(t[i])

# stream will hold data points
stream, = ax.plot([], [], '.-', lw=1, ms=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
history_x, history_y = deque(maxlen=stream_count), deque(maxlen=stream_count)

# animates the graph
def animate(i):
    # could think of this as the front drop
    thisx = x[i]
    thisy = y[i]

    # resets the graph
    if i == 0:
        history_x.clear()
        history_y.clear()

    # adds to the stream
    history_x.appendleft(thisx)
    history_y.appendleft(thisy)
    stream.set_data(history_x, history_y)
    
    time_text.set_text(time_template % (i*dt))
    return stream, time_text


ani = animation.FuncAnimation(
    fig, animate, len(y), interval=dt*1000, blit=True)

plt.show()