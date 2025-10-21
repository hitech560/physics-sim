# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager as fm, rcParams

# ========== 样式 & 字体 ==========
# plt.style.use("dark_background")
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

# ========== 动画参数 ==========
FRAMES = 150     # 总帧数
FPS = 15

def simulate_gauge_2d():
    # ---- 网格与时间步 ----
    Nx, Ny = 64, 64
    Lx, Ly = 6.4, 6.4          # 物理尺寸（任意单位）
    dx, dy = Lx/Nx, Ly/Ny
    c = 1.0                    # 光速（单位化）
    dt = 0.65 * dx / (c*np.sqrt(2))  # 满足 CFL 稳定约束

    # ---- 场变量 ----
    Ax = np.zeros((Nx, Ny))
    Ay = np.zeros((Nx, Ny))
    Ax_prev = Ax.copy()
    Ay_prev = Ay.copy()

    # ---- 初始激发：高斯包络 + 少量噪声 ----
    x = (np.arange(Nx) - Nx/2) * dx
    y = (np.arange(Ny) - Ny/2) * dy
    X, Y = np.meshgrid(x, y, indexing='ij')
    r2 = X**2 + Y**2
    sigma2 = (0.6**2)
    Ax[:] = np.exp(-r2/(2*sigma2)) * np.cos(3*X) + 0.02*np.random.randn(Nx, Ny)
    Ay[:] = np.exp(-r2/(2*sigma2)) * np.sin(3*Y) + 0.02*np.random.randn(Nx, Ny)
    Ax_prev[:] = Ax
    Ay_prev[:] = Ay

    # ---- 工具：二维拉普拉斯（周期边界） ----
    def laplacian(Z):
        return (
            np.roll(Z,  1, axis=0) + np.roll(Z, -1, axis=0) +
            np.roll(Z,  1, axis=1) + np.roll(Z, -1, axis=1) - 4*Z
        ) / (dx*dx)  # 这里假设 dx=dy；若不同可分开写

    # ---- 物理量：Bz、能量密度 ----
    def Bz_from_A(Ax, Ay):
        dAy_dx = (np.roll(Ay, -1, axis=0) - np.roll(Ay, 1, axis=0)) / (2*dx)
        dAx_dy = (np.roll(Ax, -1, axis=1) - np.roll(Ax, 1, axis=1)) / (2*dx)
        return dAy_dx - dAx_dy

    def energy_density(Ax, Ay, Ax_prev, Ay_prev):
        Ex = -(Ax - Ax_prev)/dt
        Ey = -(Ay - Ay_prev)/dt
        dAx_dx = (np.roll(Ax, -1, 0) - np.roll(Ax, 1, 0))/(2*dx)
        dAx_dy = (np.roll(Ax, -1, 1) - np.roll(Ax, 1, 1))/(2*dx)
        dAy_dx = (np.roll(Ay, -1, 0) - np.roll(Ay, 1, 0))/(2*dx)
        dAy_dy = (np.roll(Ay, -1, 1) - np.roll(Ay, 1, 1))/(2*dx)
        grad2 = dAx_dx**2 + dAx_dy**2 + dAy_dx**2 + dAy_dy**2
        return 0.5*(Ex**2 + Ey**2 + (c**2)*grad2)

    # ---- 动画绘制 ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    im1 = ax1.imshow(Bz_from_A(Ax, Ay), cmap="RdBu", origin="lower",
                     vmin=-1.0, vmax=1.0, interpolation="nearest")
    ax1.set_title("Bz = ∂xAy − ∂yAx")
    im2 = ax2.imshow(energy_density(Ax, Ay, Ax_prev, Ay_prev),
                     cmap="RdBu", origin="lower",
                     vmin=0.0, vmax=1.0, interpolation="nearest")
    ax2.set_title(r"能量密度 $\mathcal{E}$")
    plt.tight_layout()

    def animate(_frame):
        nonlocal Ax, Ay, Ax_prev, Ay_prev
        # 2D 波动方程的 leapfrog 更新
        Ax_new = 2*Ax - Ax_prev + (c*dt)**2 * laplacian(Ax)
        Ay_new = 2*Ay - Ay_prev + (c*dt)**2 * laplacian(Ay)

        Ax_prev, Ax = Ax, Ax_new
        Ay_prev, Ay = Ay, Ay_new

        im1.set_data(Bz_from_A(Ax, Ay))
        im2.set_data(energy_density(Ax, Ay, Ax_prev, Ay_prev))
        return im1, im2

    ani = FuncAnimation(fig, animate, frames=FRAMES, interval=1000/FPS, blit=True)

    # === 保存 GIF（需要 Pillow） ===
    ani.save("gauge2d.gif", dpi=120, writer="pillow", fps=FPS)
    # 如需保存：ani.save("gauge2d.mp4", fps=30)  # 需安装 ffmpeg
    # from matplotlib.animation import FFMpegWriter
    # ani.save("gauge2d.mp4", writer=FFMpegWriter(fps=FPS, bitrate=2400), dpi=150)

    plt.show()

if __name__ == "__main__":
    simulate_gauge_2d()
