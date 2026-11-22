import numpy as np
import matplotlib.pyplot as plt

# ---- Part A: resolution numbers ----
for bits in [12, 19]:
    steps = 2**bits                    # steps per full turn
    res_deg = 360 / steps              # one step in degrees
    res_arcsec = res_deg * 3600        # one step in arcseconds
    print(f"{bits}-bit: {steps} steps, {res_deg:.6f} deg, {res_arcsec:.2f} arcsec")

# tip movement on a 1 m arm for one 19-bit step
res_rad = np.deg2rad(360 / 2**19)      # one step in radians
print(f"19-bit step on 1 m arm = {1.0 * res_rad * 1e6:.2f} micrometres")

# ---- Part B: see what an encoder does to the angle ----
bits = 6                               # tiny encoder so you can SEE the steps
step = 360 / 2**bits                   # 5.625 degrees per step
true_angle = np.linspace(0, 360, 1000) # the real shaft angle, smooth
reading = np.around(true_angle / step) * step   # encoder can only report whole steps

plt.plot(true_angle, true_angle, label="true angle")
plt.plot(true_angle, reading, label=f"{bits}-bit encoder reading")
plt.xlabel("True shaft angle [deg]")
plt.ylabel("Angle [deg]")
plt.legend()
plt.grid()
plt.show()
error = reading - true_angle           # how wrong the encoder is at each angle

plt.plot(true_angle, error)
plt.xlabel("True shaft angle [deg]")
plt.ylabel("Error = reading - true [deg]")
plt.title(f"{bits}-bit encoder quantisation error")
plt.grid()
plt.show()
