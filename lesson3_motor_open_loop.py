import numpy as np
import matplotlib.pyplot as plt

# ---- motor values ----
V  = 12.0       # supply voltage [V]
R  = 1.2        # resistance [ohm]
L  = 0.0015     # inductance [H]
kt = 0.08       # torque constant [Nm/A]
J  = 0.00008    # inertia [kg m^2]
b  = 0.00001    # friction [Nm s/rad]

# ---- simulation: tiny time steps ----
dt = 0.00001                 # 10 microseconds per step
t = np.arange(0, 0.1, dt)   # simulate 100 ms
i = 0.0                      # current starts at 0
w = 0.0                      # speed starts at 0
I, W = [], []                # lists to store results

for _ in t:
    di = (V - R*i - kt*w) / L        # electrical equation, solved for di/dt
    dw = (kt*i - b*w) / J            # mechanical equation, solved for dw/dt
    i = i + di*dt                    # new current = old + change in this step
    w = w + dw*dt                    # new speed   = old + change in this step
    I.append(i)
    W.append(w)

print(f"Peak current:   {max(I):.2f} A")
print(f"Final speed:    {W[-1]:.1f} rad/s = {W[-1]*60/(2*np.pi):.0f} rpm")
print(f"Final current:  {I[-1]:.4f} A")

fig, ax = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
ax[0].plot(t*1000, W); ax[0].set_ylabel("Speed [rad/s]"); ax[0].grid()
ax[1].plot(t*1000, I, color="orange"); ax[1].set_ylabel("Current [A]"); ax[1].grid()
ax[1].set_xlabel("Time [ms]")
fig.suptitle("DC motor switched on at 12 V (no controller)")
plt.tight_layout()
plt.show()