import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def dxdy_ellip(XY, wt, A=0.2, ellip=1.0, theta=np.pi/4):
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
ellip = 1.0
theta = np.pi / 4       # × polarization
Npoints = 16
frames = 100
A0 = 1.0

# Ring of particles
th = np.linspace(0, 2*np.pi, Npoints, endpoint=False)
X0 = A0 * np.cos(th)
Y0 = A0 * np.sin(th)

# Special point indices
#ix = np.argmin(np.abs(th - 0))               # ~ (1, 0)
#iy = np.argmin(np.abs(th - np.pi/2))         # ~ (0, 1)

# Grid setup
grid_range = np.linspace(-1.5, 1.5, 9)
gx, gy = np.meshgrid(grid_range, grid_range)
gx = gx.flatten()
gy = gy.flatten()

# Set up plot
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Grid lines
grid_lines = []
for val in grid_range:
    line_v, = ax.plot([], [], color='lightgray', lw=0.8)  # vertical
    grid_lines.append(line_v)
    line_h, = ax.plot([], [], color='lightgray', lw=0.8)  # horizontal
    grid_lines.append(line_h)

# Ring particles
points, = ax.plot([], [], 'o', color='tab:blue', markersize=5)

# Reference lines
line_x, = ax.plot([], [], color='red', lw=2, label='(1,0)')
line_y, = ax.plot([], [], color='green', lw=2, label='(0,1)')

# Update function
def update(frame):
    wt = 2 * np.pi * frame / frames

    # Deform ring
    dX, dY = dxdy_ellip([X0, Y0], wt, A=A, ellip=ellip, theta=theta)
    X = X0 + dX
    Y = Y0 + dY
    points.set_data(X, Y)

    # Reference lines
   # line_x.set_data([0, X[ix]], [0, Y[ix]])
   # line_y.set_data([0, X[iy]], [0, Y[iy]])

    # Deform and draw grid lines
    for i, val in enumerate(grid_range):
        # Vertical
        yvals = np.linspace(-1.5, 1.5, 100)
        xvals = np.full_like(yvals, val)
        dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
        grid_lines[2*i].set_data(xvals + dx, yvals + dy)

        # Horizontal
        xvals = np.linspace(-1.5, 1.5, 100)
        yvals = np.full_like(xvals, val)
        dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
        grid_lines[2*i + 1].set_data(xvals + dx, yvals + dy)

    return [points, line_x, line_y] + grid_lines

# Create animation
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
plt.show()

# Save the animation
ani.save("anims/ring_cross_polarization_with_grid.gif", writer='pillow', fps=20)

plt.close()