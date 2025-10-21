import sympy as sp

def yang_mills_lagrangian_nonabelian(Nc: int = 3):
    """
    非阿贝尔杨–米尔斯拉格朗日量（分量求和版本），返回符号化的 L。
    - Nc: 颜色指标个数（如 SU(2) 取 3，SU(3) 取 8；这里可自由指定正整数）
    约定:
      * 坐标 x0..x3，Minkowski 度规 η = diag(1,-1,-1,-1)
      * 颜色 Kronecker δ_ab 已在求和中体现为对同一 a 的平方和
      * 结构常数 f^{abc} 用 IndexedBase('f') 表示（保持完全符号）
    """

    # 1) 坐标与度规
    x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3', real=True)
    coords = (x0, x1, x2, x3)
    eta = sp.diag(1, -1, -1, -1)  # Minkowski metric

    # 2) 颜色指标与结构常数 f^{abc}，耦合常数 g
    g = sp.symbols('g', real=True)
    f = sp.IndexedBase('f')  # f[a,b,c]

    # 3) 规范势 A^a_mu(x) ：为每个 (a, mu) 创建一个独立的标量函数 A[a][mu](x)
    #    A[a][mu] 是一个调用后的 Function -> SymPy Expr，可直接微分
    A = [[sp.Function(f"A{a}_{mu}")(*coords) for mu in range(4)] for a in range(Nc)]

    # 4) 构建 F^a_{μν} = ∂_μ A^a_ν - ∂_ν A^a_μ + g f^{abc} A^b_μ A^c_ν
    F = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(Nc)]
    for a in range(Nc):
        for mu in range(4):
            for nu in range(4):
                d_mu_A_nu = sp.diff(A[a][nu], coords[mu])
                d_nu_A_mu = sp.diff(A[a][mu], coords[nu])
                comm = 0
                # 颜色求和：b,c = 0..Nc-1
                for b in range(Nc):
                    for c in range(Nc):
                        comm += f[a, b, c] * A[b][mu] * A[c][nu]
                F[a][mu][nu] = sp.simplify(d_mu_A_nu - d_nu_A_mu + g * comm)

    # 5) 升指标：F^{a,μν} = η^{μα} η^{νβ} F^a_{αβ}
    F_up = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(Nc)]
    for a in range(Nc):
        for mu in range(4):
            for nu in range(4):
                s = 0
                for alpha in range(4):
                    for beta in range(4):
                        s += eta[mu, alpha] * eta[nu, beta] * F[a][alpha][beta]
                F_up[a][mu][nu] = sp.simplify(s)

    # 6) 收缩得到 L = -1/4 * sum_a sum_{μ,ν} F^a_{μν} F^{a,μν}
    contraction = 0
    for a in range(Nc):
        for mu in range(4):
            for nu in range(4):
                contraction += F[a][mu][nu] * F_up[a][mu][nu]

    L = -sp.Rational(1, 4) * sp.simplify(contraction)
    return sp.simplify(L)

if __name__ == "__main__":
    # 例：Nc=3（如 SU(2) 的 3 个生成元；若想 SU(3) 可改为 Nc=8）
    L = yang_mills_lagrangian_nonabelian(Nc=3)
    print("杨–米尔斯拉格朗日量（非阿贝尔，分量求和）:")
    sp.pprint(L, use_unicode=True)
