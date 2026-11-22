import numpy as np

R, L, kt, J, b = 1.2, 0.0015, 0.08, 0.00002, 0.00001
V_MAX = 24.0
target = 100.0
dt = 0.00001
t = np.arange(0, 0.1, dt)

# ---------- 1. simulate one controller (same code as before) ----------
def simulate(Kp, Ki, anti_windup):
    i = w = 0.0
    integral = 0.0
    W = []
    for _ in t:
        error = target - w
        V_wanted = Kp * error + Ki * integral
        V = np.clip(V_wanted, -V_MAX, V_MAX)
        if (not anti_windup) or (V == V_wanted):
            integral += error * dt
        di = (V - R*i - kt*w) / L
        dw = (kt*i - b*w) / J
        i += di*dt
        w += dw*dt
        W.append(w)
    return np.array(W)

# ---------- 2. measure the 4 numbers ----------
def step_metrics(t, y, target):
    t10 = t[np.argmax(y >= 0.1 * target)]          # first time y reaches 10 %
    t90 = t[np.argmax(y >= 0.9 * target)]          # first time y reaches 90 %
    rise_ms = (t90 - t10) * 1000

    overshoot = max(0, (y.max() - target) / target * 100)

    outside = np.where(np.abs(y - target) > 0.02 * target)[0]   # all points outside +/-2 %
    if len(outside) == 0:
        settle_ms = 0.0                            # always inside
    elif outside[-1] == len(y) - 1:
        settle_ms = float("inf")                   # still outside at the end = never settled
    else:
        settle_ms = t[outside[-1] + 1] * 1000      # first point after the LAST time outside

    ss_error = abs(target - y[-1])
    return {"rise_ms": rise_ms, "overshoot_%": overshoot,
            "settle_ms": settle_ms, "ss_error": ss_error}

# ---------- 3. requirements and PASS/FAIL ----------
limits = {"rise_ms": 5, "overshoot_%": 15, "settle_ms": 20, "ss_error": 1}

controllers = {
    "P only (Kp=0.5)":      (0.5, 0,   False),
    "PI (Ki=100)":          (0.5, 100, False),
    "PI + anti-windup":     (0.5, 100, True),
}

for name, (Kp, Ki, aw) in controllers.items():
    y = simulate(Kp, Ki, aw)
    m = step_metrics(t, y, target)
    print(f"\n=== {name} ===")
    all_pass = True
    for key, value in m.items():
        ok = value <= limits[key]
        all_pass = all_pass and ok
        print(f"  {key:12s} {value:8.2f}   limit {limits[key]:>4}   {'PASS' if ok else 'FAIL'}")
    print(f"  OVERALL: {'PASS' if all_pass else 'FAIL'}")