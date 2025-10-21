# 🎬 科学可视化演示合集

本项目包含两个高质量的物理可视化演示，用于教学与展示：
1. **[宇称不守恒](https://zh.wikipedia.org/wiki/%E5%AE%87%E7%A7%B0%E4%B8%8D%E5%AE%88%E6%81%92)演示（Parity Violation Visualization）**  
2. **二维规范场演化模拟（2D Gauge Field Evolution Simulation）**

---

> 
> “很幸运能够在海滩上捡到了几个美丽的石头、蚌壳和螺蛳，不过，世界上更美丽的蚌壳、螺蛳、石头还多得很，还有无数多的事情需要继续做下去。”
> 
> 以此致敬[杨振宁](https://zh.wikipedia.org/zh-hans/%E6%9D%A8%E6%8C%AF%E5%AE%81)先生

## 🧭 目录

- [背景介绍](#背景介绍)
- [1️⃣ 宇称不守恒演示](#1️⃣-宇称不守恒演示)
  - [物理背景](#🧪-物理背景)
  - [模型公式](#⚙️-模型公式)
  - [动画设计](#🎨-动画设计)
  - [运行与录制](#🧰-运行与录制)
  - [输出效果](#🎞️-输出效果)
- [2️⃣ 二维规范场演化模拟](#2️⃣-二维规范场演化模拟)
  - [数学模型](#🧮-数学模型)
  - [外源激发与吸收边界](#🌊-外源激发与吸收边界)
  - [能量守恒分析](#🔋-能量守恒分析)
  - [动画与保存](#🎥-动画与保存)
  - [输出效果](#📊-输出效果)
- [环境依赖](#⚙️-环境依赖)
- [引用与参考](#🔗-引用与参考)
- [许可](#📜-许可)

---

## 背景介绍

本项目展示了两种典型的**理论物理可视化**：

| 模块 | 描述 | 学科方向 |
|------|------|----------|
| 宇称不守恒（β 衰变） | 展示弱相互作用中宇称破缺的角分布差异 | 粒子物理 / 对称性 |
| 2D 规范场演化 | 模拟类[杨–米尔斯场](https://zh.wikipedia.org/wiki/%E6%A5%8A-%E7%B1%B3%E7%88%BE%E6%96%AF%E7%90%86%E8%AB%96)的二维波动与能量扩散 | 场论 / 数值物理 |

这些可视化可直接用于：
- 高能物理教学与研讨会展示；
- 科普或讲座视频动画；
- 计算物理演示与 GPU 数值模拟前的原型验证。

---

## 1️⃣ 宇称不守恒演示

文件：`parity_violation_presentation.py`

### 🧪 物理背景

弱相互作用（β 衰变）中，宇称对称性（Parity Symmetry）被破坏。  
1956 年[吴健雄](https://zh.wikipedia.org/wiki/%E5%90%B4%E5%81%A5%E9%9B%84)（Chien-Shiung Wu）实验首次观测到这一现象：  
> β 电子更倾向于沿核自旋**反方向**发射。

### ⚙️ 模型公式

角分布：

$$
I(\theta) = (\cos^2 \theta + 0.5) \times (1 + a \cos \theta)
$$

其中：
- $a = 0$ ：宇称守恒  
- $a > 0$ ：宇称破缺程度  
- $a(t)$ 在动画中周期性变化，形成“呼吸感”

### 🎨 动画设计

| 元素 | 描述 |
|------|------|
| 🎥 双极坐标图 | 左：守恒分布；右：不守恒分布 |
| 💫 动态参数 $a(t)$ | 余弦调制的往返变化 |
| 💨 呼吸动画 | 整体半径轻微脉动 |
| ✨ Glow 效果 | 不守恒曲线带柔光脉冲 |
| 🧭 注释箭头 | “核自旋 ↑”、“电子发射方向 ↓” |
| 🕶️ 主题 | 暗色背景、发光标注、动态标题与说明字幕 |

### 🧰 运行与录制

```bash
# 实时预览（交互窗口）
python parity_violation_presentation.py

# 录制 10 秒 1080p 60fps MP4（无窗口）
python parity_violation_presentation.py --record parity.mp4 --seconds 10 --fps 60 --no-show

# 录制 GIF（30fps）
python parity_violation_presentation.py --record parity.gif --fps 30
```

### 🎞️ 输出效果

| 模式 | 内容 |
|------|------|
| 🎬 动画 | Glow 发光曲线、呼吸节奏、参数标签实时变化 |
| 🧭 标签 | “核自旋 ↑”、“电子发射方向 ↓”、“β 衰变” |
| 💡 背景 | 暗色高对比度，适合投影演示或视频嵌入 |

---

## 2️⃣ 二维规范场演化模拟

文件：`gauge_field_simulation_2d_up.py`

### 🧮 数学模型

该模拟基于简化的二维规范场（U(1) 或近似 SU(2)）形式：

$$
F_{xy} = \partial_x A_y - \partial_y A_x
$$

Lagrangian（能量密度）：

$$
\mathcal{E} = \frac{1}{2} (A_x^2 + A_y^2) + \frac{1}{2} B_z^2
$$

空间为离散网格 $(N_x \times N_y)$，时间步长 $\Delta t$ 控制演化稳定性。

### 🌊 外源激发与吸收边界

- **中心外源（Gaussian Pulse）**：  
  模拟一个高斯波包在规范场中传播。
- **吸收边界层（Absorbing Layer）**：  
  使用指数阻尼函数抑制反射波，模拟“开放边界”。

### 🔋 能量守恒分析

右侧图实时显示：
- 全域能量曲线（含吸收层）
- 内部能量曲线（不含吸收层）
> 可用于观察能量耗散与传播规律。

### 🎥 动画与保存

运行：

```bash
python gauge_field_simulation_2d_up.py
```

可选输出动画：

```bash
python gauge_field_simulation_2d_up.py --record out.gif
```

每帧包含：
1. 左图：磁场分量 $B_z = \partial_x A_y - \partial_y A_x$
2. 中图：能量密度分布 $\mathcal{E}$
3. 右图：能量曲线随时间演化

### 📊 输出效果

| 图像 | 含义 |
|------|------|
| 🌈 左：Bz 分布 | 表示局域“场强旋涡” |
| 🔮 中：能量密度 | 高亮区域代表激发传播与耗散 |
| 📈 右：能量曲线 | 展示能量守恒与衰减过程 |

动画可保存为 `out.gif` 或 `out.mp4`，支持 90–240 帧自定义。

---

## ⚙️ 环境依赖

推荐环境：Python ≥ 3.10  
核心依赖：
```bash
pip install numpy matplotlib pillow
# 若要导出 mp4：
pip install ffmpeg-python
```

| 模块 | 功能 |
|------|------|
| numpy | 数值计算与矩阵操作 |
| matplotlib | 绘图与动画引擎 |
| pillow | GIF 导出支持 |
| ffmpeg | MP4 导出支持（系统级） |

---

## 🔗 引用与参考

- C.S. Wu et al., *Experimental Test of Parity Conservation in Beta Decay*, Phys. Rev. (1957)
- Yang, C.N. & Mills, R.L., *Conservation of Isotopic Spin and Gauge Invariance*, Phys. Rev. (1954)
- S. Coleman, *Gauge Theory Lectures* (1975)
- Python Matplotlib Animation 官方文档

---

## 📜 许可

本项目遵循 MIT License 开源协议。  
可自由使用、修改和展示，但需保留署名。

> © 2025 Jerry Liu — “Physics meets Art.”  
> 欢迎用于教学、研究与公众科普展示。
