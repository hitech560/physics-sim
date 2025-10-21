# -*- coding: utf-8 -*-
import os, sys, argparse
import numpy as np
import matplotlib
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

def simulate_gauge_2d_absorbing(args):
    # ===== 网格与时间步 =====
    Nx, Ny = 96, 96
    Lx, Ly = 9.6, 9.6
    dx, dy = Lx / Nx, Ly / Ny
    c = 1.0
    dt = 0.65 * dx / (c * np.sqrt(2))  # CFL
    steps = args.frames

    # ===== 场变量 =====
    Ax = np.zeros((Nx, Ny)); Ay = np.zeros((Nx, Ny))
    Vx = np.zeros_like(Ax);  Vy = np.zeros_like(Ay)

    # 初始条件：高斯小扰动
    x = (np.arange(Nx) - Nx/2) * dx
    y = (np.arange(Ny) - Ny/2) * dy
    X, Y = np.meshgrid(x, y, indexing='ij')
    r2 = X**2 + Y**2
    Ax[:] = np.exp(-r2/(2*0.6**2)) * np.cos(2.5*X)
    Ay[:] = np.exp(-r2/(2*0.6**2)) * np.sin(2.0*Y)

    # ===== 吸收边界 =====
    w = 12
    gamma_max = 2.5
    def ramp_1d(n, w, m):
        d = np.minimum(np.arange(n), np.arange(n)[::-1])
        g = np.clip((w - d)/w, 0.0, 1.0)**3
        return m*g
    gx = ramp_1d(Nx, w, gamma_max)[:, None]
    gy = ramp_1d(Ny, w, gamma_max)[None, :]
    gamma = np.maximum(gx, gy)

    # ===== 外源 =====
    cx, cy = Nx//2, Ny//2
    drive_amp, drive_omega = 1.5, 1.0
    def source(n):
        s = np.zeros_like(Ax)
        s[cx, cy] = drive_amp * np.sin(drive_omega * n * dt)
        return s, np.zeros_like(Ax)

    # ===== 差分工具 =====
    def laplacian(Z):
        L = np.zeros_like(Z)
        L[1:-1,1:-1] = (Z[2:,1:-1]+Z[:-2,1:-1]+Z[1:-1,2:]+Z[1:-1,:-2]-4*Z[1:-1,1:-1])/(dx*dx)
        return L

    def Bz_from_A(Ax, Ay):
        dAy_dx = np.zeros_like(Ay); dAx_dy = np.zeros_like(Ax)
        dAy_dx[1:-1,:] = (Ay[2:,:] - Ay[:-2,:])/(2*dx)
        dAx_dy[:,1:-1] = (Ax[:,2:] - Ax[:,:-2])/(2*dx)
        return dAy_dx - dAx_dy

    def energy_density(Ax, Ay, Vx, Vy):
        dAx_dx = np.zeros_like(Ax); dAx_dy = np.zeros_like(Ax)
        dAy_dx = np.zeros_like(Ay); dAy_dy = np.zeros_like(Ay)
        dAx_dx[1:-1,:] = (Ax[2:,:] - Ax[:-2,:])/(2*dx)
        dAx_dy[:,1:-1] = (Ax[:,2:] - Ax[:,:-2])/(2*dx)
        dAy_dx[1:-1,:] = (Ay[2:,:] - Ay[:-2,:])/(2*dx)
        dAy_dy[:,1:-1] = (Ay[:,2:] - Ay[:,:-2])/(2*dx)
        grad2 = dAx_dx**2 + dAx_dy**2 + dAy_dx**2 + dAy_dy**2
        E2 = Vx**2 + Vy**2
        return 0.5*(E2 + (c**2)*grad2)

    mask_inner = np.ones((Nx, Ny), dtype=bool)
    mask_inner[:w,:] = mask_inner[-w:,:] = False
    mask_inner[:, :w] = mask_inner[:, -w:] = False

    # ===== 画布 =====
    fig = plt.figure(figsize=(14, 4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1,1,1])
    ax_bz  = fig.add_subplot(gs[0,0])
    ax_en  = fig.add_subplot(gs[0,1])
    ax_cur = fig.add_subplot(gs[0,2])

    im_bz = ax_bz.imshow(Bz_from_A(Ax, Ay), origin="lower",
                         cmap="RdBu", vmin=-1.0, vmax=1.0, interpolation="nearest")
    ax_bz.set_title("Bz = ∂xAy − ∂yAx")
    im_en = ax_en.imshow(energy_density(Ax, Ay, Vx, Vy), origin="lower",
                         cmap="magma", vmin=0.0, vmax=2.0, interpolation="nearest")
    ax_en.set_title(r"能量密度 $\mathcal{E}$")
    ax_cur.set_title("能量曲线"); ax_cur.set_xlabel("步数"); ax_cur.set_ylabel("能量（求和）")
    (line_all,)   = ax_cur.plot([], [], label="全域能量")
    (line_inner,) = ax_cur.plot([], [], label="内部能量（不含海绵层）")
    ax_cur.legend(loc="best"); ax_cur.grid(True)

    energy_all_hist, energy_inner_hist = [], []

    # ===== 动画步进 =====
    def step(n):
        nonlocal Ax, Ay, Vx, Vy
        Sx, Sy = source(n)
        den = (1 + 0.5*gamma*dt)

        Vx = ((1 - 0.5*gamma*dt)*Vx + dt*((c**2)*laplacian(Ax) + Sx)) / den
        Vy = ((1 - 0.5*gamma*dt)*Vy + dt*((c**2)*laplacian(Ay) + Sy)) / den
        Ax = Ax + dt*Vx
        Ay = Ay + dt*Vy

        Bz = Bz_from_A(Ax, Ay)
        En = energy_density(Ax, Ay, Vx, Vy)
        im_bz.set_data(Bz); im_en.set_data(En)

        energy_all_hist.append(np.sum(En)*dx*dy)
        energy_inner_hist.append(np.sum(En[mask_inner])*dx*dy)
        line_all.set_data(np.arange(len(energy_all_hist)), energy_all_hist)
        line_inner.set_data(np.arange(len(energy_inner_hist)), energy_inner_hist)
        ax_cur.relim(); ax_cur.autoscale_view()
        return im_bz, im_en, line_all, line_inner

    ani = FuncAnimation(fig, step, frames=steps, interval=1000/args.fps, blit=False)

    # ===== 录制 =====
    if args.record:
        out = args.record
        root, ext = os.path.splitext(out)
        ext = ext.lower()
        if ext == ".mp4":
            try:
                from matplotlib.animation import FFMpegWriter
                writer = FFMpegWriter(fps=args.fps, bitrate=args.bitrate)
            except Exception as e:
                raise RuntimeError("保存 .mp4 需要已安装 ffmpeg。") from e
            ani.save(out, writer=writer, dpi=args.dpi)
        elif ext == ".gif":
            from matplotlib.animation import PillowWriter
            ani.save(out, writer=PillowWriter(fps=args.fps), dpi=args.dpi)
        else:
            raise ValueError("不支持的扩展名：请用 .mp4 或 .gif")

    if not args.no_show:
        plt.show()
    else:
        plt.close(fig)

def parse_args():
    p = argparse.ArgumentParser(description="2D 规范场演化（外源 + 吸收边界 + 能量曲线）")
    p.add_argument("--record", type=str, default="",
                   help="输出文件名（.mp4 或 .gif）。如提供则自动录制。")
    p.add_argument("--fps", type=int, default=30, help="帧率")
    p.add_argument("--frames", type=int, default=800, help="总帧数")
    p.add_argument("--dpi", type=int, default=120, help="保存时的 DPI")
    p.add_argument("--bitrate", type=int, default=1800, help="mp4 比特率 kbps（FFmpeg）")
    p.add_argument("--no-show", action="store_true",
                   help="仅录制不弹窗（适合服务器/自动化）")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()

    # 若仅录制且不需要 GUI，使用无界面后端
    if args.record and args.no_show:
        matplotlib.use("Agg")  # 必须在导入 pyplot 之前，但这里已导入；仅当脚本顶层使用更稳
        # 这个分支如果需要严格无窗，建议把 use("Agg") 提到文件最顶部、在 import pyplot 之前。

    simulate_gauge_2d_absorbing(args)
