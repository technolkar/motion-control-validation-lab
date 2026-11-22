import numpy as np
import matplotlib.pyplot as plt

R, L, kt, J, b = 1.2, 0.0015, 0.08, 0.00002, 0.00001
V_MAX = 24.0
W_MAX = 150.0                       # speed limit for the position loop [rad/s]
Kp_w, Ki_w = 0.5, 100               # INNER speed loop: your PI from Lesson 3
target = np.pi / 2                  # 90 degrees in radians

dt = 0.00001
t = np.arange(0, 0.1, dt)           # 100 ms

for Kx in [30, 300, 1000, 3000]:    # OUTER position loop gain
    i = w = x = 0.0                 # x = shaft angle [rad]
    integral = 0.0
    X = []
    for _ in t:
        # ---- outer loop: position -> wanted speed ----
        w_ref = np.clip(Kx * (target - x), -W_MAX, W_MAX)
        # ---- inner loop: speed PI with anti-windup -> voltage ----
        error = w_ref - w
        V_wanted = Kp_w * error + Ki_w * integral
        V = np.clip(V_wanted, -V_MAX, V_MAX)
        if V == V_wanted:
            integral += error * dt
        # ---- motor ----
        di = (V - R*i - kt*w) / L
        dw = (kt*i - b*w) / J
        i += di*dt
        w += dw*dt
        x += w*dt                   # NEW: angle = sum of speed over time
        X.append(np.degrees(x))
    print(f"Kx = {Kx:5}: final angle {X[-1]:6.2f} deg, max {max(X):6.1f} deg")
    plt.plot(t*1000, X, label=f"Kx = {Kx}")

plt.axhline(90, color="black", linestyle="--", label="target 90 deg")
plt.xlabel("Time [ms]")
plt.ylabel("Shaft angle [deg]")
plt.title("Cascade: position P-loop around PI speed loop")
plt.legend()
plt.grid()
plt.show()