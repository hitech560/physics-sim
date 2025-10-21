import numpy as np

def R6v(u, eta):
    """
    6-vertex/XXZ 模型的 R(u)，满足参数化 YBE（任意常数 eta）。
    取无关紧要的整体因子为 1：
        R(u) = [[a, 0, 0, 0],
                [0, b, c, 0],
                [0, c, b, 0],
                [0, 0, 0, a]]
      其中 a = sinh(u+eta), b = sinh(u), c = sinh(eta)
    """
    a = np.sinh(u + eta)
    b = np.sinh(u)
    c = np.sinh(eta)
    R = np.array([[a, 0, 0, 0],
                  [0, b, c, 0],
                  [0, c, b, 0],
                  [0, 0, 0, a]], dtype=float)
    return R

def kron3(A, B, C):
    return np.kron(np.kron(A, B), C)

def verify_ybe(u, v, w, eta, atol=1e-12):
    I2 = np.eye(2)
    R_u_v = R6v(u - v, eta)      # R(u-v)
    R_u_w = R6v(u - w, eta)      # R(u-w)
    R_v_w = R6v(v - w, eta)      # R(v-w)

    # 8x8: R12(x) = R(x) ⊗ I, R23(x) = I ⊗ R(x)
    R12_uv = np.kron(R_u_v, I2)
    R23_vw = np.kron(I2, R_v_w)

    # 交换算子（相邻两个因子）P ∈ C^2⊗C^2
    P = np.array([[1, 0, 0, 0],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1]], dtype=float)

    S12 = np.kron(P, I2)   # 8x8
    S23 = np.kron(I2, P)   # 8x8

    # R13(x) = S23 · (R12(x)) · S23   （或者 S12 · (R23(x)) · S12）
    R13_uw = S23 @ (np.kron(R_u_w, I2)) @ S23

    LHS = R12_uv @ R13_uw @ R23_vw
    RHS = R23_vw @ R13_uw @ R12_uv

    diff_norm = np.linalg.norm(LHS - RHS)
    ok = np.allclose(LHS, RHS, atol=atol)

    return ok, diff_norm

if __name__ == "__main__":
    eta = 0.7      # 各向异性参数（Δ = cosh(eta)/2 一类，不影响 YBE 成立）
    u, v, w = 0.3, -0.4, 0.9  # 任取谱参数
    ok, nrm = verify_ybe(u, v, w, eta)
    print("6-vertex 参数化 YBE 验证：")
    print(f"||LHS - RHS||_F = {nrm:.3e}")
    print("✅ 成立" if ok else "❌ 不成立")
