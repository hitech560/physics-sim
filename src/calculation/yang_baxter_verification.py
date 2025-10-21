import numpy as np

def yang_baxter_verification():
    """
    验证（常数）杨–巴克斯特方程：R12 R13 R23 = R23 R13 R12
    注意：你给的 R(alpha) 未必对任意 alpha 满足 YBE，这里主要先修正维度与构造。
    """

    # --- 6-vertex/XXZ 风格的一个常数 R(alpha)（你的写法保持不变） ---
    def R_matrix(alpha):
        return np.array([
            [1, 0, 0, 0],
            [0, np.sinh(alpha), np.cosh(alpha), 0],
            [0, np.cosh(alpha), np.sinh(alpha), 0],
            [0, 0, 0, 1]
        ], dtype=float)

    # --- 两比特的 SWAP（置换）算子 P：交换相邻两个因子 ---
    P = np.array([
        [1,0,0,0],
        [0,0,1,0],
        [0,1,0,0],
        [0,0,0,1]
    ], dtype=float)

    I2 = np.eye(2)
    alpha = 0.5

    R = R_matrix(alpha)

    # 8x8：R12 = R ⊗ I,  R23 = I ⊗ R
    R12 = np.kron(R, I2)
    R23 = np.kron(I2, R)

    # 8x8 交换算子：S12 = P ⊗ I,  S23 = I ⊗ P
    S12 = np.kron(P, I2)
    S23 = np.kron(I2, P)

    # 正确的 8x8：R13 = S23 · (R ⊗ I) · S23  （等价地：S12 · (I ⊗ R) · S12）
    R13 = S23 @ R12 @ S23
    # R13 = S12 @ R23 @ S12  # 用这行也可以

    # 左右两边
    LHS = R12 @ R13 @ R23
    RHS = R23 @ R13 @ R12

    print("杨–巴克斯特方程（常数版）验证：")
    print("||LHS - RHS||_F =", np.linalg.norm(LHS - RHS))

    if np.allclose(LHS, RHS, atol=1e-10):
        print("✅ 等式成立（在给定数值精度下）")
    else:
        print("⚠️  等式不成立：这组 R(alpha) 非通解；alpha=0 时退化为 I，等式自然成立。")

if __name__ == "__main__":
    yang_baxter_verification()
