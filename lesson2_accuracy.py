import numpy as np
import matplotlib.pyplot as plt

# ---- the mechanical setup ----
e = 10e-6        # eccentricity: disc is 10 micrometres off-centre [m]
R = 0.04         # sensor reads the disc at 20 mm radius [m]

# ---- error amplitude by formula ----
amp_rad = e / R                          # angle error in radians
amp_arcsec = np.rad2deg(amp_rad) * 3600  # radians -> degrees -> arcsec
print(f"Eccentricity error amplitude: {amp_rad:.6f} rad = {amp_arcsec:.1f} arcsec")
print(f"That is {amp_arcsec / 2.47:.0f} x the 19-bit resolution")

# ---- error over two full turns ----
angle_deg = np.linspace(0, 720, 2000)    # two revolutions
theta = np.deg2rad(angle_deg)            # sin() needs radians
error_arcsec = amp_arcsec * np.sin(theta)    # one sine wave per revolution

plt.plot(angle_deg, error_arcsec)
plt.xlabel("True shaft angle [deg]  (2 turns)")
plt.ylabel("Encoder error [arcsec]")
plt.title(f"Eccentricity error, e = {e*1e6:.0f} um")
plt.grid()
plt.show()