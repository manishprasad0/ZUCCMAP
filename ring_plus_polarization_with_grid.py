import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

# Deformation function for gravitational wave (smooth transition from circular)
def dxdy_ellip(XY, wt, A=0.2, ellip=1.0, theta=0):
    # Apply the deformation smoothly as a function of wt
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
theta = 0         # 0 for +, pi/4 for ×
Npoints = 16
frames = 100
initial_radius = 1.0  # Renamed for clarity

# Ring of particles
th = np.linspace(0, 2*np.pi, Npoints, endpoint=False)
X0 = initial_radius * np.cos(th)
Y0 = initial_radius * np.sin(th)

# Special point indices (for reference lines)
ix = np.argmin(np.abs(th - 0))               # ~ (1, 0)
iy = np.argmin(np.abs(th - np.pi/2))         # ~ (0, 1)

# Grid setup (no changes)
grid_range = np.linspace(-1.5, 1.5, 9)
gx, gy = np.meshgrid(grid_range, grid_range)
gx = gx.flatten()
gy = gy.flatten()

# Set up plot with higher DPI
fig, ax = plt.subplots(figsize=(5, 5), dpi=200)  # Set DPI to 200 for higher quality
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Grid lines (no changes)
grid_lines = []
for val in grid_range:
    # Vertical lines
    line_v, = ax.plot([], [], color='lightgray', lw=0.8)
    grid_lines.append(line_v)
    # Horizontal lines
    line_h, = ax.plot([], [], color='lightgray', lw=0.8)
    grid_lines.append(line_h)

# Ring particles (blue color initially)
points = ax.scatter([], [], color='tab:blue', s=50)  # Use scatter instead of plot for points

# Reference lines
line_x, = ax.plot([], [], color='red', lw=2, label='(1,0)')
line_y, = ax.plot([], [], color='red', lw=2, label='(0,1)')

# Update function for the animation
def update(frame):
    wt = 2 * np.pi * frame / frames

    # Deform ring positions smoothly from a circular shape
    dX, dY = dxdy_ellip([X0, Y0], wt, A=A, ellip=ellip, theta=theta)
    X = X0 + dX
    Y = Y0 + dY
    points.set_offsets(np.column_stack((X, Y)))  # Update particle positions

    # Highlight the points at (1, 0) and (0, 1) in red
    colors = [mcolors.to_rgba('tab:blue', alpha=0.3)] * Npoints  # Set blue to 30% opacity
    colors[ix] = 'red'  # Set the point at (1, 0) to red
    colors[iy] = 'red'  # Set the point at (0, 1) to red
    points.set_facecolor(colors)  # Update the color of the points

    # Reference lines
    line_x.set_data([0, X[ix]], [0, Y[ix]])
    line_y.set_data([0, X[iy]], [0, Y[iy]])

    # Deform and draw grid lines
    for i, val in enumerate(grid_range):
        # Vertical line at x=val
        yvals = np.linspace(-1.5, 1.5, 100)
        xvals = np.full_like(yvals, val)
        dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
        grid_lines[2*i].set_data(xvals + dx, yvals + dy)

        # Horizontal line at y=val
        xvals = np.linspace(-1.5, 1.5, 100)
        yvals = np.full_like(xvals, val)
        dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
        grid_lines[2*i + 1].set_data(xvals + dx, yvals + dy)

    return [points, line_x, line_y] + grid_lines

# Create animation (set blit=False to avoid resizing issues)
ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

# Display animation
plt.show()

# To save the animation
ani.save("anims/ring_plus_polarization_with_grid.gif", writer='pillow', fps=20)