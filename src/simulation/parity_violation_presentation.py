# -*- coding: utf-8 -*-
"""
parity_violation_presentation.py
展示级“宇称不守恒”动画：暗色主题 + Glow + 动态箭头 + a(t) 标签 + 1080p 录制
用法示例：
  python parity_violation_presentation.py --record parity.mp4 --seconds 12 --fps 60 --no-show
  python parity_violation_presentation.py --record parity.gif --fps 30
"""
import os, argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager as fm, rcParams

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="Parity Violation Presentation Animation")
    p.add_argument("--record", type=str, default="",
                   help="输出文件名（.mp4 或 .gif）。留空则不保存。")
    p.add_argument("--fps", type=int, default=60, help="帧率（默认60）")
    p.add_argument("--seconds", type=float, default=10.0, help="动画总时长（秒）")
    p.add_argument("--dpi", type=int, default=150, help="保存/显示 DPI（默认150）")
    p.add_argument("--width", type=int, default=1920, help="输出像素宽（默认1920）")
    p.add_argument("--height", type=int, default=1080, help="输出像素高（默认1080）")
    p.add_argument("--amax", type=float, default=0.8, help="不对称参数最大值 A_MAX（默认0.8）")
    p.add_argument("--breath", type=float, default=0.06, help="呼吸幅度（默认0.06）")
    p.add_argument("--no-show", action="store_true", help="仅录制不弹窗")
    return p.parse_args()

# ---------- 样式与中文字体 ----------
plt.style.use("dark_background")
def set_chinese_font():
    preferred = ["Microsoft YaHei", "微软雅黑", "SimHei", "黑体",
                 "Noto Sans CJK SC", "WenQuanYi Zen Hei"]
    installed = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            rcParams["font.sans-serif"] = [name]
            break
    rcParams["axes.unicode_minus"] = False
    rcParams["mathtext.fontset"] = "stix"
    rcParams["mathtext.default"] = "regular"
set_chinese_font()

# ---------- 角分布模型 ----------
def parity_distributions(theta, a=0.6):
    # 守恒：cos^2 θ + 0.5；不守恒：乘 (1 + a cos θ)
    pc = np.cos(theta)**2 + 0.5
    pv = pc * (1 + a * np.cos(theta))
    return pc, pv

def main():
    args = parse_args()

    # 无界面渲染（仅录制时可选）：必须在 import pyplot 前设置；此处已导入，只作为提醒
    if args.record and args.no_show:
        # 若需要严格无窗渲染，请把下面两行移到文件顶部（在 import pyplot 之前）
        matplotlib.use("Agg")

    # Figure 尺寸（按像素与 DPI 计算英寸）
    fig_w = args.width / args.dpi
    fig_h = args.height / args.dpi

    # ---------- 画布 ----------
    fig, (ax1, ax2) = plt.subplots(
        1, 2, subplot_kw=dict(projection="polar"),
        figsize=(fig_w, fig_h), constrained_layout=True
    )

    # 极坐标设置
    for ax in (ax1, ax2):
        ax.set_theta_zero_location("N")  # 0° 在正上
        ax.set_theta_direction(-1)       # 顺时针
        ax.grid(color=(1, 1, 1, 0.25))
        # 更清爽的外观
        ax.set_rlabel_position(135)

    # 数据与基线
    theta = np.linspace(0, 2*np.pi, 1600)
    pc_ref, _ = parity_distributions(theta, a=0.0)

    # 左侧：守恒（蓝）
    line_pc, = ax1.plot(theta, pc_ref, color="#69b3ff", lw=3.0, alpha=0.95)
    ax1.set_title("宇称守恒情况", pad=14)

    # 右侧：不守恒（红）
    # 先画 Glow（多条线作为光晕）
    glow_colors = ["#ff6a5c"]*3
    glow_lws    = [10.0, 7.0, 4.5]
    glow_alphas = [0.12, 0.20, 0.35]
    glow_lines  = []
    _, pv0 = parity_distributions(theta, a=0.0)
    for c, lw, al in zip(glow_colors, glow_lws, glow_alphas):
        ln, = ax2.plot(theta, pv0, color=c, lw=lw, alpha=al, solid_capstyle="round")
        glow_lines.append(ln)
    # 主曲线
    line_pv, = ax2.plot(theta, pv0, color="#ff6a5c", lw=3.2, alpha=0.98)
    title_right = ax2.set_title("宇称不守恒情况（β 衰变）  a=0.00", pad=14)

    # 动态箭头与标签
    spin_len = 1.2
    emit_len = 0.8
    spin_anno = ax2.annotate("", xy=(0.0, spin_len), xytext=(0.0, 0.0),
                             arrowprops=dict(arrowstyle="-|>", lw=2.6, color="w", alpha=0.95))
    ax2.text(0.0, spin_len*1.06, "核自旋 ↑", ha="center", va="bottom",
             color="w", fontsize=14)
    emit_anno = ax2.annotate("", xy=(np.pi, emit_len), xytext=(np.pi, 0.0),
                             arrowprops=dict(arrowstyle="-|>", lw=2.6, color="#ffdd66", alpha=0.95))
    emit_label = ax2.text(np.pi, emit_len*1.06, "电子发射方向 ↓", ha="center", va="top",
                          color="#ffdd66", fontsize=14)

    # 放到 ax2 里，用轴坐标(0-1)定位到右上角
    param_box = ax2.text(
        0.98, 0.98, "a = 0.00",
        transform=ax2.transAxes, ha="right", va="top",
        fontsize=14, color="#ffdd66",
        bbox=dict(boxstyle="round,pad=0.3", fc=(0.2,0.2,0.2,0.6), ec="#ffdd66")
    )

    # 说明字幕（静态）仍然用 fig.text，但【不要】放进 animate 的返回值里
    caption = fig.text(
        0.5, 0.04,
        "吴健雄实验思想示意：β 电子更偏向与核自旋相反方向发射（宇称不守恒）",
        ha="center", va="center", color=(1,1,1,0.7), fontsize=12
    )

    # ---------- 动画参数 ----------
    total_frames = int(args.fps * args.seconds)
    A_MIN, A_MAX = 0.0, float(args.amax)
    BREATH = float(args.breath)

    def animate(frame: int):
        # 归一化时间 t∈[0,1)
        t = frame / total_frames
        # a(t) 余弦往返（平滑无尖角）
        a_t = A_MIN + (A_MAX - A_MIN) * (0.5 - 0.5*np.cos(2*np.pi*t))
        # 呼吸尺度
        scale = 1.0 + BREATH * np.sin(2*np.pi*t)

        # 左：守恒，仅呼吸
        line_pc.set_ydata(pc_ref * scale)

        # 右：不守恒 + 呼吸
        _, pv = parity_distributions(theta, a=a_t)
        pv_scaled = pv * scale
        line_pv.set_ydata(pv_scaled)
        for ln in glow_lines:
            ln.set_ydata(pv_scaled)

        # Glow 脉冲：alpha 随时间小幅起伏
        pulse = 0.5 + 0.5*np.sin(2*np.pi*t)
        for ln, base_alpha in zip(glow_lines, glow_alphas):
            ln.set_alpha(base_alpha*(0.75 + 0.5*pulse))

        # 箭头显著性随 a 增强
        lw = 2.2 + 3.0*(a_t / max(A_MAX, 1e-9))
        alpha = 0.55 + 0.45*(a_t / max(A_MAX, 1e-9))
        emit_anno.arrow_patch.set_linewidth(lw)
        emit_anno.arrow_patch.set_alpha(alpha)
        emit_label.set_alpha(alpha)

        # 轻微拉伸长度增强动感
        spin_anno.xy = (0.0,  spin_len*(0.95 + 0.1*scale))
        emit_anno.xy = (np.pi, emit_len*(0.95 + 0.1*scale))
        emit_label.set_position((np.pi, emit_len*(1.06 + 0.12*(scale-1))))

        # 动态标题 & 参数标签
        title_right.set_text(f"宇称不守恒情况（β 衰变）  a={a_t:.2f}")
        # animate() 内更新 param_box 文本
        param_box.set_text(f"a = {a_t:.2f}")

        # animate() 的返回值里，移除 caption（它是 fig 级别），只返回 axes 级别的对象
        return (*glow_lines, line_pc, line_pv, spin_anno, emit_anno, emit_label, title_right, param_box)

    # 动画
    interval_ms = 1000.0 / args.fps
    ani = FuncAnimation(fig, animate, frames=total_frames, interval=interval_ms, blit=True)

    # ---------- 录制 ----------
    if args.record:
        root, ext = os.path.splitext(args.record)
        ext = ext.lower()
        if ext == ".mp4":
            try:
                from matplotlib.animation import FFMpegWriter
                writer = FFMpegWriter(fps=args.fps, bitrate=2800)
            except Exception as e:
                raise RuntimeError("保存 .mp4 需要已安装 ffmpeg。") from e
            ani.save(args.record, writer=writer, dpi=args.dpi)
        elif ext == ".gif":
            from matplotlib.animation import PillowWriter
            ani.save(args.record, writer=PillowWriter(fps=args.fps), dpi=args.dpi)
        else:
            raise ValueError("不支持的扩展名：请使用 .mp4 或 .gif")

    if not args.no_show:
        plt.show()
    else:
        plt.close(fig)

if __name__ == "__main__":
    main()
