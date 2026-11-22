import numpy as np
import matplotlib.pyplot as plt

# ---- motor values (light load again) ----
R, L, kt, J, b = 1.2, 0.0015, 0.08, 0.00002, 0.00001
V_MAX = 24.0                  # supply limit [V]
target = 100.0                # wanted speed [rad/s]

dt = 0.00001
t = np.arange(0, 0.05, dt)    # 50 ms

for Kp in [0.5, 2, 10]:       # try three different gains
    i = w = 0.0
    W = []
    for _ in t:
        error = target - w                         # how far from target
        V = np.clip(Kp * error, -V_MAX, V_MAX)     # P controller, limited to +/-24 V
        di = (V - R*i - kt*w) / L                  # motor equations (same as before)
        dw = (kt*i - b*w) / J
        i += di*dt
        w += dw*dt
        W.append(w)
    print(f"Kp = {Kp:4}:  final speed {W[-1]:6.2f} rad/s,  steady-state error {target - W[-1]:5.2f} rad/s")
    plt.plot(t*1000, W, label=f"Kp = {Kp}")

plt.axhline(target, color="black", linestyle="--", label="target 100")
plt.xlabel("Time [ms]")
plt.ylabel("Speed [rad/s]")
plt.title("P speed control")
plt.legend()
plt.grid()
plt.show()