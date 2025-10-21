import numpy as np
from itertools import product

def stress(eta_vals=(0.7,1.1), u_vals=(-1, -0.2, 0.0, 0.3, 1.2)):
    from ybe_6vertex import verify_ybe  # 或把函数粘到同文件
    fails = []
    for eta, u, v, w in product(eta_vals, u_vals, u_vals, u_vals):
        ok, nrm = verify_ybe(u, v, w, eta)
        if not ok:
            fails.append((eta, u, v, w, nrm))
    print("All good!" if not fails else f"Fails: {fails}")

if __name__ == "__main__":
    stress()
