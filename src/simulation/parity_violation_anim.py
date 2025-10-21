# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager as fm, rcParams

# ========== 样式 & 字体 ==========
plt.style.use("dark_background")
def set_cn():
    preferred = ["Microsoft YaHei", "微软雅黑", "SimHei", "黑体",
                 "Noto Sans CJK SC", "WenQuanYi Zen Hei"]
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            rcParams["font.sans-serif"] = [name]
            break
    rcParams["axes.unicode_minus"] = False
set_cn()

# ========== 角分布模型 ==========
def parity_distributions(theta, a=0.6):
    # 守恒：cos^2θ + 0.5； 不守恒：乘以 (1 + a cosθ)
    pc = np.cos(theta)**2 + 0.5
    pv = pc * (1 + a * np.cos(theta))
    return pc, pv

# ========== 画布 ==========
theta = np.linspace(0, 2*np.pi, 1200)
pc0, pv0 = parity_distributions(theta, a=0.0)

fig, (ax1, ax2) = plt.subplots(
    1, 2, subplot_kw=dict(projection="polar"), figsize=(12, 6), constrained_layout=True
)
for ax in (ax1, ax2):
    ax.set_theta_zero_location("N")  # 0° 在正上方
    ax.set_theta_direction(-1)       # 顺时针
    ax.grid(color=(1, 1, 1, 0.25))

line_pc, = ax1.plot(theta, pc0, color="#69b3ff", lw=2.5)
ax1.set_title("宇称守恒情况", pad=16)

line_pv, = ax2.plot(theta, pv0, color="#ff6a5c", lw=2.8)
ax2.set_title("宇称不守恒情况（β 衰变）  a=0.00", pad=16)

# 动态箭头与标签
spin_len = 2.2
emit_len = 2.2
spin_anno = ax2.annotate("", xy=(0.0, spin_len), xytext=(0.0, 0.0),
                         arrowprops=dict(arrowstyle="-|>", lw=2.4, color="w", alpha=0.9))
ax2.text(0.0, spin_len*1.06, "核自旋 ↑", ha="center", va="bottom", color="w", fontsize=12)

emit_anno = ax2.annotate("", xy=(np.pi, emit_len), xytext=(np.pi, 0.0),
                         arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#ffdd66", alpha=0.9))
emit_label = ax2.text(np.pi, emit_len*1.06, "电子发射方向 ↓", ha="center", va="top",
                      color="#ffdd66", fontsize=12)

# ========== 动画参数 ==========
FRAMES = 300     # 总帧数
FPS = 30
A_MIN, A_MAX = 0.0, 0.8
BREATH = 0.06
pc_ref, _ = parity_distributions(theta, a=0.0)

def animate(i):
    t = i / FRAMES
    a = A_MIN + (A_MAX - A_MIN) * (0.5 - 0.5*np.cos(2*np.pi*t))  # 平滑往返
    scale = 1.0 + BREATH * np.sin(2*np.pi*t)                     # 呼吸

    # 左图：守恒，仅呼吸
    line_pc.set_ydata(pc_ref * scale)

    # 右图：不守恒 + 呼吸
    _, pv = parity_distributions(theta, a=a)
    line_pv.set_ydata(pv * scale)
    ax2.set_title(f"宇称不守恒情况（β 衰变）  a={a:.2f}", pad=16)

    # 箭头显著性随 a 增强
    lw = 2.0 + 3.0*(a / max(A_MAX, 1e-9))
    alpha = 0.5 + 0.5*(a / max(A_MAX, 1e-9))
    emit_anno.arrow_patch.set_linewidth(lw)
    emit_anno.arrow_patch.set_alpha(alpha)
    emit_label.set_alpha(alpha)

    # 轻微拉伸长度增强动感
    spin_anno.xy = (0.0, spin_len * (0.95 + 0.1*scale))
    emit_anno.xy = (np.pi, emit_len * (0.95 + 0.1*scale))
    emit_label.set_position((np.pi, emit_len * (1.06 + 0.12*(scale-1))))

    return line_pc, line_pv, spin_anno, emit_anno, emit_label

ani = FuncAnimation(fig, animate, frames=FRAMES, interval=1000/FPS, blit=True)

# === 保存 GIF（需要 Pillow） ===
# ani.save("parity_violation.gif", dpi=120, writer="pillow", fps=FPS)

# 如需保存 MP4（需要 ffmpeg）：取消下行注释
# from matplotlib.animation import FFMpegWriter
# ani.save("parity_violation.mp4", writer=FFMpegWriter(fps=FPS, bitrate=2400), dpi=150)

plt.show()
