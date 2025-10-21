import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def gauge_field_simulation():
    """
    模拟 2D 规范场的演化（简化模型）
    """

    # 参数设置
    Nx, Ny = 50, 50
    dx, dy = 0.1, 0.1
    dt = 0.01
    steps = 100

    # 初始化规范场 A（二维矢量场）
    A_x = np.zeros((Nx, Ny))
    A_y = np.zeros((Nx, Ny))
    A_x_prev = np.zeros_like(A_x)
    A_y_prev = np.zeros_like(A_y)

    # 设定初始条件（局部激发）
    A_x[Nx // 2, Ny // 2] = 1.0
    A_y[Nx // 2, Ny // 2] = 1.0

    # 时间演化
    def update_step(n):
        # 简化演化方程：波动方程形式
        nonlocal A_x, A_y

        A_x_new = (
            2 * A_x - A_x_prev
            + (dt / dx) ** 2
              * (np.roll(A_x, 1, axis=0) + np.roll(A_x, -1, axis=0) - 2 * A_x)
            + (dt / dy) ** 2
              * (np.roll(A_x, 1, axis=1) + np.roll(A_x, -1, axis=1) - 2 * A_x)
        )

        A_y_new = (
            2 * A_y - A_y_prev
            + (dt / dx) ** 2
              * (np.roll(A_y, 1, axis=0) + np.roll(A_y, -1, axis=0) - 2 * A_y)
            + (dt / dy) ** 2
              * (np.roll(A_y, 1, axis=1) + np.roll(A_y, -1, axis=1) - 2 * A_y)
        )

        A_x_prev[:], A_x[:] = A_x, A_x_new
        A_y_prev[:], A_y[:] = A_y, A_y_new
        return A_x, A_y

    # 动画绘制
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    im1 = ax[0].imshow(A_x, cmap='RdBu', animated=True)
    im2 = ax[1].imshow(A_y, cmap='RdBu', animated=True)

    def animate(frame):
        A_x, A_y = update_step(frame)
        im1.set_array(A_x)
        im2.set_array(A_y)
        return im1, im2

    ani = FuncAnimation(fig, animate, frames=steps, interval=50, blit=True)
    plt.show()

# 注意：实际运行需处理边界条件与稳定性，此处为简化演示
if __name__ == "__main__":
    gauge_field_simulation()