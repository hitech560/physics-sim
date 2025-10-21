# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager as fm, rcParams

# ---------- 样式 & 字体 ----------
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

# ---------- 物理模型 ----------
def parity_distributions(theta, asymmetry=0.6):
    """返回宇称守恒与不守恒的角分布"""
    parity_conserved = np.cos(theta)**2 + 0.5
    parity_violated  = parity_conserved * (1 + asymmetry * np.cos(theta))
    return parity_conserved, parity_violated

# ---------- 画布与静态曲线 ----------
theta = np.linspace(0, 2*np.pi, 1000)
pc, pv = parity_distributions(theta, asymmetry=0.6)

fig, (ax1, ax2) = plt.subplots(
    1, 2, subplot_kw=dict(projection='polar'), figsize=(10, 5), constrained_layout=True
)

# 左：宇称守恒（静态）
line_pc, = ax1.plot(theta, pc, color='tab:blue', linewidth=2)
ax1.set_title("宇称守恒情况", pad=16)

# 右：宇称不守恒（动画）
line_pv, = ax2.plot(theta, pv, color='tab:red', linewidth=2)
title_right = ax2.set_title("宇称不守恒情况（β 衰变）", pad=16)

# ---------- 动画：让不对称参数在 [0, 0.8] 循环变化 ----------
A_MIN, A_MAX = 0.0, 0.8
FPS = 30
STEPS = 240  # 帧数

def anim_asymmetry(frame):
    # 平滑往返：0 -> 1 -> 0
    t = frame / STEPS
    a = A_MIN + (A_MAX - A_MIN) * (0.5 - 0.5*np.cos(2*np.pi*t))  # 余弦缓动
    _, pv_dyn = parity_distributions(theta, asymmetry=a)
    line_pv.set_ydata(pv_dyn)
    # ax2.set_title(f"宇称不守恒情况（β 衰变）  a={a:.2f}", pad=16)
    title_right.set_text(f"宇称不守恒情况（β 衰变）  a={a:.2f}")
    # print(title_right)
    return (line_pv,)

ani = FuncAnimation(fig, anim_asymmetry, frames=STEPS, interval=1000/FPS, blit=True)

plt.show()

# 如需保存动画，解除下面一行注释（需要安装 ffmpeg 或 pillow）：
# ani.save("parity_violation.gif", dpi=120)   # 或 .mp4
