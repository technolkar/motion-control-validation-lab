import numpy as np
import matplotlib.pyplot as plt

N = 4096                                            # samples in ONE turn
angle_deg = np.linspace(0, 360, N, endpoint=False)  # exactly one revolution
theta = np.deg2rad(angle_deg)

rng = np.random.default_rng(0)
total = 103 * np.sin(theta) + 30 * np.sin(2 * theta + 1.0) + rng.normal(0, 5, N)

# ---- FFT: split the total into harmonics ----
spectrum = np.abs(np.fft.rfft(total)) * 2 / N   # size of each harmonic in arcsec
for k in range(1, 6):
    print(f"H{k}: {spectrum[k]:6.1f} arcsec")

# ---- plots ----
fig, ax = plt.subplots(2, 1, figsize=(9, 7))
ax[0].plot(angle_deg, total, color="red")
ax[0].set_xlabel("True shaft angle [deg] (one turn)")
ax[0].set_ylabel("Total error [arcsec]")
ax[0].grid()

k = np.arange(1, 11)                 # harmonics 1..10
ax[1].bar(k, spectrum[1:11])
ax[1].set_xticks(k)
ax[1].set_xlabel("Harmonic (waves per turn)")
ax[1].set_ylabel("Amplitude [arcsec]")
ax[1].grid()
plt.tight_layout()
plt.show()