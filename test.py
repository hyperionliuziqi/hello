from manim import *
import numpy as np

class QuantumTunneling(ThreeDScene):
    def construct(self):
        # 1. 设置坐标系
        axes = ThreeDAxes()
        
        # 势阱函数 (U型剖面)
        def pit_func(x):
            return 0.2 * x**2

        # 使用 Surface 代替 ParametricSurface
        pit_3d = Surface(
            lambda u, v: np.array([u, v, 0.2 * (u**2 + v**2)]),
            u_range=[-3, 3], v_range=[-3, 3],
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.6
        )

        # 2D 剖面曲线
        pit_curve = axes.plot(pit_func, x_range=[-4, 4], color=BLUE)

        # --- 第一阶段：3D展示势阱与经典小球 ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.play(Create(pit_3d), run_time=2)
        
        # 经典小球 (Sphere 在 3D 中效果更好)
        ball = Sphere(radius=0.2, color=RED).move_to(axes.c2p(-2, 0, pit_func(-2)))
        self.add(ball)

        # 模拟小球在势阱中滚动 (经典物理：无法越过边缘)
        path_tracker = ValueTracker(-2)
        ball.add_updater(lambda m: m.move_to(axes.c2p(path_tracker.get_value(), 0, pit_func(path_tracker.get_value()))))
        
        # 来回摆动两次
        self.play(path_tracker.animate.set_value(2), run_time=1.5, rate_func=there_and_back)
        self.play(path_tracker.animate.set_value(2), run_time=1.5, rate_func=there_and_back)
        ball.clear_updaters()

        # --- 第二阶段：3D转2D剖面 ---
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0) # 停止任何潜在旋转
        self.wait(0.5)
        
        # 移除 3D 曲面，显示 2D 曲线
        self.play(
            FadeOut(pit_3d),
            Create(pit_curve),
            ball.animate.move_to(axes.c2p(-2, 0, 0)) # 将球降到 2D 平面
        )
        
        # 绘制势垒（墙壁）
        barrier = Rectangle(width=0.8, height=3, fill_opacity=0.8, color=GREY_B).move_to(axes.c2p(2, 1.5, 0))
        barrier_label = Text("势垒", font_size=24, color=GREY_B).next_to(barrier, UP)
        self.play(Create(barrier), Write(barrier_label))

        # --- 第三阶段：经典转量子 (概率云) ---
        # 创建一团点云
        cloud = VGroup(*[Dot(radius=0.04, color=WHITE) for _ in range(100)])
        cloud.move_to(ball.get_center())
        
        def update_cloud(m):
            for dot in m:
                # 在球体中心附近随机分布
                dot.move_to(ball.get_center() + np.random.normal(0, 0.35, 3))
                dot.set_opacity(np.random.random())

        self.play(FadeOut(ball), FadeIn(cloud))
        cloud.add_updater(update_cloud)
        
        # 概率云向墙移动
        self.play(ball.animate.move_to(axes.c2p(1.5, 0, 0)), run_time=2)
        self.wait(1)
        cloud.remove_updater(update_cloud)

        # --- 第四阶段：波函数与隧穿 ---
        self.play(FadeOut(cloud), FadeOut(pit_curve))
        
        # 定义波函数参数
        b_start = 1.6  # 墙左侧
        b_end = 2.4    # 墙右侧
        k = 8          # 波数
        kappa = 4      # 衰减系数
        time_tracker = ValueTracker(0)

        def get_wave():
            t = time_tracker.get_value()
            def wave_logic(x):
                if x < b_start:
                    # 入射波
                    return 0.6 * np.sin(k * x - t)
                elif b_start <= x <= b_end:
                    # 势垒内指数衰减 (连续性衔接)
                    amp_at_edge = 0.6 * np.sin(k * b_start - t)
                    return amp_at_edge * np.exp(-kappa * (x - b_start))
                else:
                    # 隧穿后的微弱波
                    amp_at_exit = 0.6 * np.sin(k * b_start - t) * np.exp(-kappa * (b_end - b_start))
                    return amp_at_exit * np.sin(k * (x - b_end) + (k * b_start - t))

            return axes.plot(wave_logic, x_range=[-4, 5], color=YELLOW)

        wave_mobject = always_redraw(get_wave)
        self.add(wave_mobject)
        
        # 播放波函数动画
        self.play(time_tracker.animate.set_value(15), run_time=8, rate_func=linear)

        # 标注隧穿现象
        arrow = Arrow(start=axes.c2p(3.5, 1, 0), end=axes.c2p(3, 0.2, 0), color=RED)
        tunnel_text = Text("量子隧穿", color=RED, font_size=30).next_to(arrow, UP)
        self.play(Create(arrow), Write(tunnel_text))
        
        self.wait(2)