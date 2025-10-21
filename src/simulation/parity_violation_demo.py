import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams

# plt.style.use("dark_background")
def set_chinese_font():
    preferred = ["Microsoft YaHei", "微软雅黑", "SimHei", "黑体", "Noto Sans CJK SC", "WenQuanYi Zen Hei"]
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            rcParams["font.sans-serif"] = [name]
            break
    else:
        # 找不到也能正常显示英文字体，但提示一下
        print("⚠ 未发现常见中文字体，可能仍会出现乱码。")
    # 解决负号显示为方块的问题
    rcParams["axes.unicode_minus"] = False
set_chinese_font()

def parity_violation_simulation():
    """
    模拟弱相互作用中宇称不守恒的角分布
    显示 β 衰变中电子发射相对于核自旋方向的不对称性
    """

    theta = np.linspace(0, 2 * np.pi, 1000)

    # 理想宇称守恒情况：对称分布
    parity_conserved = np.cos(theta)**2 + 0.5

    # 宇称不守恒情况：不对称分布（基于 Wu 实验简化模型）
    asymmetry = 0.6  # 不对称参数
    parity_violated = parity_conserved * (1 + asymmetry * np.cos(theta))

    # 极坐标绘图
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))

    ax1.plot(theta, parity_conserved, 'b', linewidth=2)
    ax1.set_title('宇称守恒情况', pad=20)

    ax2.plot(theta, parity_violated, 'r', linewidth=2)
    ax2.set_title('宇称不守恒情况（β 衰变）', pad=20)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parity_violation_simulation()
