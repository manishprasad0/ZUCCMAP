import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Deformation function for elliptical polarization
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
ellip = 1.0       # + polarization
theta = 0         # 0 for +, pi/4 for ×
Npoints = 16
frames = 100
A0 = 1.0

# Initial ring of particles
th = np.linspace(0, 2*np.pi, Npoints, endpoint=False)
X0 = A0 * np.cos(th)
Y0 = A0 * np.sin(th)

# Indices for (1, 0) and (0, 1)
ix = np.argmin(np.abs(th - 0))               # Closest to (1, 0)
iy = np.argmin(np.abs(th - np.pi/2))         # Closest to (0, 1)

# Set up the plot
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Ring points
points, = ax.plot([], [], 'o', color='tab:blue', markersize=5)

# Lines from origin to two special points
line_x, = ax.plot([], [], color='red', lw=2, label='(1,0)')
line_y, = ax.plot([], [], color='red', lw=2, label='(0,1)')

# Animation update function
def update(frame):
    wt = 2 * np.pi * frame / frames
    dX, dY = dxdy_ellip([X0, Y0], wt, A=A, ellip=ellip, theta=theta)
    X = X0 + dX
    Y = Y0 + dY

    points.set_data(X, Y)

    # Update dynamic lines
    line_x.set_data([0, X[ix]], [0, Y[ix]])
    line_y.set_data([0, X[iy]], [0, Y[iy]])

    return points, line_x, line_y

# Create and save animation
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
plt.show()

ani.save("anims/ring_plus_polarization_ligo.gif", writer='pillow', fps=20)