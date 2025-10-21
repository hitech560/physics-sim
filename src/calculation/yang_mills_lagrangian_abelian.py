import sympy as sp

def yang_mills_lagrangian_abelian():
    """
    构建（Abelian 版本）杨–米尔斯/麦克斯韦场的拉格朗日量:
        L = -1/4 F_{μν} F^{μν}
    这里将 A_μ 当作标量函数（Abelian 情况, commutator=0）。
    """

    # 1) 坐标与度规
    x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3', real=True)
    coords = (x0, x1, x2, x3)

    # Minkowski metric diag(1, -1, -1, -1)
    eta = sp.diag(1, -1, -1, -1)
    eta_inv = eta  # 对于对角矩阵，其逆矩阵恰好相同（同一对角元素的倒数）

    # 2) 规范势的四个分量 A_μ(x)
    A0 = sp.Function('A0')(*coords)
    A1 = sp.Function('A1')(*coords)
    A2 = sp.Function('A2')(*coords)
    A3 = sp.Function('A3')(*coords)
    A = [A0, A1, A2, A3]

    # 3) 构建场强张量 F_{μν} = ∂_μ A_ν - ∂_ν A_μ  （Abelian：忽略 i g [A_μ, A_ν]）
    F = sp.MutableDenseNDimArray.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            d_mu_A_nu = sp.diff(A[nu], coords[mu])
            d_nu_A_mu = sp.diff(A[mu], coords[nu])
            F[mu, nu] = d_mu_A_nu - d_nu_A_mu

    # 4) 升指标：F^{μν} = η^{μα} η^{νβ} F_{αβ}
    #    这等价于 F_up = eta * F * eta  的分量写法（注意这里把张量当矩阵双边“夹”）
    #    我们直接按定义显式求和，便于与上面数组对齐
    F_up = sp.MutableDenseNDimArray.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            s = 0
            for alpha in range(4):
                for beta in range(4):
                    s += eta[mu, alpha] * eta[nu, beta] * F[alpha, beta]
            F_up[mu, nu] = sp.simplify(s)

    # 5) 收缩得到 L = -1/4 F_{μν} F^{μν}
    contraction = 0
    for mu in range(4):
        for nu in range(4):
            contraction += F[mu, nu] * F_up[mu, nu]

    L = -sp.Rational(1, 4) * sp.simplify(contraction)
    return sp.simplify(L)

if __name__ == "__main__":
    L = yang_mills_lagrangian_abelian()
    print("杨–米尔斯拉格朗日量（Abelian 简化形式）:")
    sp.pprint(L, use_unicode=True)
