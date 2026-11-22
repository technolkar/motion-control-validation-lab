import numpy as np
import matplotlib.pyplot as plt

R, L, kt, J, b = 1.2, 0.0015, 0.08, 0.00002, 0.00001
V_MAX = 24.0
target = 100.0
Kp = 0.5                          # keep P fixed, only change I

dt = 0.00001
t = np.arange(0, 0.1, dt)         # 100 ms

for Ki in [0, 20, 100, 500]:
    i = w = 0.0
    integral = 0.0                # sum of past errors, starts at 0
    W = []
    for _ in t:
        error = target - w
        integral = integral + error * dt                       # I: add up the error
        V = np.clip(Kp * error + Ki * integral, -V_MAX, V_MAX) # PI controller
        di = (V - R*i - kt*w) / L
        dw = (kt*i - b*w) / J
        i += di*dt
        w += dw*dt
        W.append(w)
    print(f"Ki = {Ki:4}: final speed {W[-1]:7.2f} rad/s,  max speed {max(W):6.1f} rad/s")
    plt.plot(t*1000, W, label=f"Ki = {Ki}")

plt.axhline(target, color="black", linestyle="--", label="target 100")
plt.xlabel("Time [ms]")
plt.ylabel("Speed [rad/s]")
plt.title(f"PI speed control (Kp = {Kp})")
plt.legend()
plt.grid()
plt.show()