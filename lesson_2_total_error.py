import numpy as np
import matplotlib.pyplot as plt

angle_deg = np.linspace(0, 720, 2000)     # two turns
theta = np.deg2rad(angle_deg)

# ---- the three error sources, in arcsec ----
ecc = 103 * np.sin(theta)                 # eccentricity: 1 wave per turn
mis = 30 * np.sin(2 * theta + 1.0)        # misalignment: 2 waves per turn (+1.0 = shifted start)
rng = np.random.default_rng(0)            # random number generator (0 = same "random" every run)
noise = rng.normal(0, 5, angle_deg.size)  # random noise, typical size 5 arcsec

total = ecc + mis + noise                 # what the testbench actually measures

# ---- numbers a validation engineer reports ----
print(f"Peak-to-peak total error: {total.max() - total.min():.1f} arcsec")

# ---- plot: each source on its own, then the total ----
fig, ax = plt.subplots(4, 1, figsize=(9, 9), sharex=True)   # 4 graphs stacked
ax[0].plot(angle_deg, ecc);   ax[0].set_ylabel("Eccentricity")
ax[1].plot(angle_deg, mis);   ax[1].set_ylabel("Misalignment")
ax[2].plot(angle_deg, noise); ax[2].set_ylabel("Noise")
ax[3].plot(angle_deg, total, color="red"); ax[3].set_ylabel("TOTAL measured")
ax[3].set_xlabel("True shaft angle [deg]")
for a in ax:
    a.grid()
fig.suptitle("Encoder error sources [arcsec]")
plt.tight_layout()
plt.show()