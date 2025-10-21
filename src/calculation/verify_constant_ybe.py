import numpy as np

def hecke_R(q: float):
    I4 = np.eye(4)
    P  = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=float)
    Rcheck = q*I4 - (1.0/q)*P     # Hecke 解
    R = P @ Rcheck                # 转成 YBE 里的 R
    return R, P

def verify_constant_ybe(q=1.3, atol=1e-12):
    R, P = hecke_R(q)
    I2 = np.eye(2)
    R12 = np.kron(R, I2)
    R23 = np.kron(I2, R)
    # R13 = S23·R12·S23
    S23 = np.kron(I2, P)
    R13 = S23 @ R12 @ S23
    LHS = R12 @ R13 @ R23
    RHS = R23 @ R13 @ R12
    nrm = np.linalg.norm(LHS - RHS)
    print("||LHS - RHS||_F =", f"{nrm:.3e}")
    print("✅" if np.allclose(LHS, RHS, atol=atol) else "❌")

if __name__ == "__main__":
    verify_constant_ybe()
