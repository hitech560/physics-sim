import sympy as sp
from sympy import tensorcontraction, tensorproduct

def yang_mills_lagrangian():
    """
    计算杨–米尔斯规范场的拉格朗日量
    返回: F_{μν} F^{μν} 的表达式
    """
    # 定义时空指标与规范场
    mu, nu = sp.symbols('mu nu', cls=sp.IndexedBase)
    A_mu = sp.Function('A')(mu)
    A_nu = sp.Function('A')(nu)

    # 定义场强张量 F_{μν} = ∂_μ A_ν - ∂_ν A_μ + i g [A_μ, A_ν]
    d_mu_A_nu = sp.Derivative(A_nu, mu)
    d_nu_A_mu = sp.Derivative(A_mu, nu)
    commutation_term = sp.I * sp.Symbol('g') * (A_mu * A_nu - A_nu * A_mu)

    F_mu_nu = d_mu_A_nu - d_nu_A_mu + commutation_term

    # 构建拉格朗日量 L = -1/4 Tr(F_{μν} F^{μν})
    F_upper = sp.tensorproduct(F_mu_nu, F_mu_nu)  # 简化处理，未做指标升降
    L = -sp.Rational(1, 4) * tensorcontraction(F_upper, (0, 1))

    return L


if __name__ == "__main__":
    lagrangian = yang_mills_lagrangian()
    print("杨–米尔斯拉格朗日量 (简化形式):")
    sp.pprint(lagrangian, use_unicode=True)
