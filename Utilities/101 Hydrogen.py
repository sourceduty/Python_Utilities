import matplotlib.pyplot as plt
import numpy as np

# Define the hydrogen atom structure
nucleus = {'protons': 1, 'neutrons': 0}
electrons = [{'n': 1, 'orbit_radius': 1}]

# Plotting the nucleus
fig, ax = plt.subplots()
ax.plot(0, 0, 'ro', label='Nucleus (Protons: 1, Neutrons: 0)')

# Plotting the electron orbit
theta = np.linspace(0, 2 * np.pi, 100)
for electron in electrons:
    x_orbit = electron['orbit_radius'] * np.cos(theta)
    y_orbit = electron['orbit_radius'] * np.sin(theta)
    ax.plot(x_orbit, y_orbit, 'b--', label=f'Electron Orbit (n={electron["n"]})')
    # Position of the electron
    ax.plot(electron['orbit_radius'], 0, 'bo', label=f'Electron (n={electron["n"]})')

# Setting plot limits and labels
ax.set_aspect('equal')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.set_title('Bohr Model of Hydrogen Atom')

# Show the plot
plt.show()
