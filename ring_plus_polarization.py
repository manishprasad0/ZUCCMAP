import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

# Displacement function: elliptical deformation
def dxdy_ellip(XY, wt, A=0.2, ellip=1.0, theta=0):
    x, y = XY
    cth, sth = np.cos(theta), np.sin(theta)
    xp = cth * x + sth * y
    yp = -sth * x + cth * y
    dxp = A * xp * np.cos(wt)
    dyp = -A * ellip * yp * np.cos(wt)
    dx = cth * dxp - sth * dyp
    dy = sth * dxp + cth * dyp
    return dx, dy

# Parameters
A = 0.2
ellip = 1.0       # 1 for "+" polarization, -1 for "×" polarization
theta = 0         # 0 for "+" polarization, pi/4 for "×"
Npoints = 16
frames = 100
A0 = 1.0

# Ring of particles
th = np.linspace(0, 2*np.pi, Npoints, endpoint=False)
X0 = A0 * np.cos(th)
Y0 = A0 * np.sin(th)

# Setup plot
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')
points, = ax.plot([], [], 'o', color='tab:blue', markersize=3)

# Animation function
def update(frame):
    wt = 2 * np.pi * frame / frames
    dX, dY = dxdy_ellip([X0, Y0], wt, A=A, ellip=ellip, theta=theta)
    points.set_data(X0 + dX, Y0 + dY)
    return points,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

#save animation
ani.save("anims/ring_plus_polarization.gif", writer='pillow', fps=20)

plt.show()