import numpy as np
import matplotlib.pyplot as plt

R, L, kt, J, b = 1.2, 0.0015, 0.08, 0.00002, 0.00001
V_MAX = 24.0
target = 100.0
Kp, Ki = 0.5, 100

dt = 0.00001
t = np.arange(0, 0.1, dt)

for anti_windup in [False, True]:          # run twice: without, then with
    i = w = 0.0
    integral = 0.0
    W, INT = [], []
    for _ in t:
        error = target - w
        V_wanted = Kp * error + Ki * integral          # what the controller asks for
        V = np.clip(V_wanted, -V_MAX, V_MAX)           # what the supply can give
        if (not anti_windup) or (V == V_wanted):       # anti-windup: only integrate if NOT at limit
            integral = integral + error * dt
        di = (V - R*i - kt*w) / L
        dw = (kt*i - b*w) / J
        i += di*dt
        w += dw*dt
        W.append(w)
        INT.append(Ki * integral)                      # the I-part in volts, to see the windup
    name = "WITH anti-windup" if anti_windup else "without anti-windup"
    print(f"{name:20s}: final {W[-1]:6.2f} rad/s, max {max(W):6.1f} rad/s, "
          f"overshoot {(max(W) - target) / target * 100:4.1f} %")
    ax1 = plt.subplot(2, 1, 1); ax1.plot(t*1000, W, label=name)
    ax2 = plt.subplot(2, 1, 2); ax2.plot(t*1000, INT, label=name)

ax1.axhline(target, color="black", linestyle="--")
ax1.set_ylabel("Speed [rad/s]"); ax1.legend(); ax1.grid()
ax2.set_ylabel("I-part [V]"); ax2.set_xlabel("Time [ms]"); ax2.legend(); ax2.grid()
plt.suptitle(f"PI control, Kp={Kp}, Ki={Ki}: effect of anti-windup")
plt.tight_layout()
plt.show()