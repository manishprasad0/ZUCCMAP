import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Feature Toggles ---
leave_trail = False              # 1. Show trailing triangle path
trace_center = False             # 2. Trace center of triangle
loop_continuously = False        # 3. Make motion loop back and forth
grid_lines_on = True             # 4. Show grid lines

# Gravitational wave deformation function (+ polarization)
def dxdy_ellip(XY, wt, A=0.1, ellip=1.0, theta=0):
    x, y = XY
    cth, sth = np.cos(theta), np.sin(theta)
    xp = cth * x + sth * y
    yp = -sth * x + cth * y
    dxp = A * xp * np.cos(wt)
    dyp = -A * ellip * yp * np.cos(wt)
    dx = cth * dxp - sth * dyp
    dy = sth * dxp + cth * dyp
    return dx, dy

# --- Parameters ---
A = 0.12
ellip = 1.0
theta = 0
frames = 200
side = 2.0
radius = side / np.sqrt(3)
arc_radius = 5.0
start_angle = 0
end_angle = np.pi / 2
spin_velocity = 4 * np.pi / frames

# Triangle shape (relative to center)
angles = np.linspace(0, 2 * np.pi, 4)[:-1] + np.pi / 2
x0 = radius * np.cos(angles)
y0 = radius * np.sin(angles)

# Grid and axes
grid_min, grid_max = -3, 9
grid_step = 1.0
grid_range = np.arange(grid_min, grid_max + grid_step, grid_step)

# Set up plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(grid_min, grid_max)
ax.set_ylim(grid_min, grid_max)
ax.set_aspect('equal')
ax.axis('off')

# Grid lines
grid_lines = []
for val in grid_range:
    line_v, = ax.plot([], [], color='lightgray', lw=0.6)
    grid_lines.append(line_v)
    line_h, = ax.plot([], [], color='lightgray', lw=0.6)
    grid_lines.append(line_h)

# Axes
x_axis, = ax.plot([], [], color='black', lw=1.0)
y_axis, = ax.plot([], [], color='black', lw=1.0)

# Triangle visuals
triangle_points, = ax.plot([], [], 'o', color='tab:blue', markersize=6)
triangle_edges, = ax.plot([], [], '-', color='tab:blue', lw=2)

# Trail setup
trail_lines = []  # list of all triangle edge lines (if leave_trail is True)
center_trace_x = []
center_trace_y = []
center_trace_line, = ax.plot([], [], color='tab:red', lw=1.5, linestyle='--') if trace_center else (None,)

# add sun
sun = plt.Circle((0, 0), 0.5, color='gold', zorder=5)
ax.add_patch(sun)

# Update function
def update(frame):
    if loop_continuously:
        # Oscillate back and forth across the arc
        phase = (frame % (2 * frames)) / frames
        alpha = phase if phase <= 1 else 2 - phase
    else:
        alpha = frame / frames

    orbit_angle = start_angle + alpha * (end_angle - start_angle)
    wt = 2 * np.pi * frame / frames

    # Triangle center position along arc
    cx = arc_radius * np.cos(orbit_angle)
    cy = arc_radius * np.sin(orbit_angle)

    # Triangle spinning about its center
    spin_angle = spin_velocity * frame
    c_spin, s_spin = np.cos(spin_angle), np.sin(spin_angle)
    x_rot = c_spin * x0 - s_spin * y0
    y_rot = s_spin * x0 + c_spin * y0

    x_total = cx + x_rot
    y_total = cy + y_rot

    # Gravitational wave deformation
    dx, dy = dxdy_ellip([x_total, y_total], wt, A=A, ellip=ellip, theta=theta)
    x_def = x_total + dx
    y_def = y_total + dy

    # Triangle edges and points
    triangle_points.set_data(x_def, y_def)
    triangle_edges.set_data(np.append(x_def, x_def[0]), np.append(y_def, y_def[0]))

    # Leave trail of previous edges
    if leave_trail:
        line, = ax.plot(np.append(x_def, x_def[0]), np.append(y_def, y_def[0]), '-', color='tab:blue', lw=1, alpha=0.3)
        trail_lines.append(line)

    # Trace center
    if trace_center:
        center_trace_x.append(cx)
        center_trace_y.append(cy)
        center_trace_line.set_data(center_trace_x, center_trace_y)

    # Grid lines
    if grid_lines_on:
        for i, val in enumerate(grid_range):
            yvals = np.linspace(grid_min, grid_max, 200)
            xvals = np.full_like(yvals, val)
            dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
            grid_lines[2 * i].set_data(xvals + dx, yvals + dy)

            xvals = np.linspace(grid_min, grid_max, 200)
            yvals = np.full_like(xvals, val)
            dx, dy = dxdy_ellip([xvals, yvals], wt, A=A, ellip=ellip, theta=theta)
            grid_lines[2 * i + 1].set_data(xvals + dx, yvals + dy)

    # Axes
    x_axis.set_data([grid_min, grid_max], [0, 0])
    y_axis.set_data([0, 0], [grid_min, grid_max])

    return [triangle_points, triangle_edges, x_axis, y_axis, *grid_lines, *trail_lines, center_trace_line] if trace_center else [triangle_points, triangle_edges, x_axis, y_axis, *grid_lines, *trail_lines]

# Create animation
total_frames = 2 * frames if loop_continuously else frames
ani = animation.FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True)
plt.show()

ani.save("anims/lisa_arc_trail.gif", writer='pillow', fps=20)