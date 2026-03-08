from manim import *
import numpy as np

class QuantumTunneling(ThreeDScene):
    def construct(self):
        # --- 1. 初始化坐标系 ---
        axes = ThreeDAxes(x_range=[-6, 6], y_range=[-6, 6], z_range=[-2, 4])
        
        # 定义势阱函数 (抛物线形)
        def pit_func_3d(u, v):
            return 0.1 * (u**2 + v**2)

        def pit_func_2d(x):
            return 0.2 * x**2

        # 3D 势阱表面
        pit_3d = Surface(
            lambda u, v: np.array([u, v, pit_func_3d(u, v)]),
            u_range=[-4, 4], v_range=[-4, 4],
            checkerboard_colors=[BLUE_D, BLUE_E], fill_opacity=0.7
        )

        # --- 2. 3D 场景：经典小球滚动 ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.play(Create(pit_3d), run_time=2)

        # 创建 3D 实心小球
        ball = Sphere(radius=0.2, color=RED).set_sheen(0.5, direction=UL)
        
        # 小球运动轨迹控制 (使用 ValueTracker 模拟简谐运动)
        time_tracker = ValueTracker(0)
        ball.add_updater(lambda m: m.move_to(axes.c2p(
            2.5 * np.cos(time_tracker.get_value() * 2), # X轴往复
            0,                                          # Y轴固定
            pit_func_3d(2.5 * np.cos(time_tracker.get_value() * 2), 0) # Z轴随深度变化
        )))

        self.add(ball)
        # 滚动约 6 秒
        self.play(time_tracker.animate.set_value(6), run_time=6, rate_func=linear)
        ball.clear_updaters()

        # --- 3. 视角转换：3D -> 2D ---
        # 准备 2D 的坑
        pit_curve = axes.plot(pit_func_2d, x_range=[-4, 4], color=BLUE_A)
        
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=3)
        self.play(
            FadeOut(pit_3d),
            Create(pit_curve),
            ball.animate.move_to(axes.c2p(-2.5, 0, pit_func_2d(-2.5))),
            run_time=2
        )
        
        # 2D 滚动演示
        self.play(path_track := ValueTracker(-2.5))
        ball.add_updater(lambda m: m.move_to(axes.c2p(
            path_track.get_value(), 0, pit_func_2d(path_track.get_value())
        )))
        self.play(path_track.animate.set_value(2.5), run_time=1.5, rate_func=there_and_back)
        ball.clear_updaters()

        # --- 4. 经典转量子：概率云 ---
        # 创建一个由大量点组成的概率云
        num_dots = 400
        cloud = VGroup(*[
            Dot(radius=0.03, color=WHITE).move_to(ball.get_center()) 
            for _ in range(num_dots)
        ])

        def update_cloud(m):
            # 模拟高斯分布的概率云
            center = ball.get_center()
            for dot in m:
                # 随机散布在中心周围，亮度随距离衰减
                offset = np.random.normal(0, 0.4, 3)
                dot.move_to(center + offset)
                dist = np.linalg.norm(offset)
                dot.set_opacity(max(0, 1 - dist/0.8))

        self.play(FadeIn(cloud), ball.animate.set_opacity(0))
        cloud.add_updater(update_cloud)
        self.play(ball.animate.move_to(axes.c2p(0, 0, 0.5)), run_time=2)
        self.wait(1)
        
        # --- 5. 波函数演化与隧穿 ---
        # 隐藏概率云，引入波函数
        self.play(FadeOut(cloud), FadeOut(pit_curve))
        
        # 势垒参数
        barrier_x = 2.0
        barrier_width = 0.6
        barrier = Rectangle(width=barrier_width, height=3, color=GREY_B, fill_opacity=0.5)\
                  .move_to(axes.c2p(barrier_x + barrier_width/2, 1, 0))
        self.play(Create(barrier))

        wave_time = ValueTracker(0)
        k = 10      # 波数
        kappa = 5   # 势垒内衰减系数

        def get_tunneling_wave():
            t = wave_time.get_value()
            def wave_func(x):
                # 1. 势垒左侧：入射波 + 反射波 (干涉形成驻波趋势)
                if x < barrier_x:
                    # 简化展示：向右行进的波包
                    return 0.8 * np.exp(-(x + 2 - t*0.5)**2) * np.sin(k * x - 5 * t)
                # 2. 势垒内部：指数衰减
                elif barrier_x <= x <= barrier_x + barrier_width:
                    amp_at_edge = 0.8 * np.exp(-(barrier_x + 2 - t*0.5)**2) * np.sin(k * barrier_x - 5 * t)
                    return amp_at_edge * np.exp(-kappa * (x - barrier_x))
                # 3. 势垒右侧：透射波 (极微弱)
                else:
                    amp_at_exit = 0.8 * np.exp(-(barrier_x + 2 - t*0.5)**2) * \
                                  np.sin(k * barrier_x - 5 * t) * np.exp(-kappa * barrier_width)
                    return amp_at_exit * np.sin(k * (x - (barrier_x + barrier_width)) + (k * barrier_x - 5 * t))

            return axes.plot(wave_func, x_range=[-5, 5], color=YELLOW)

        wave_mobject = always_redraw(get_tunneling_wave)
        self.add(wave_mobject)
        
        # 波函数向前推进并撞击
        self.play(wave_time.animate.set_value(8), run_time=6, rate_func=linear)
        
        # --- 6. 停顿与局部放大 ---
        # 停止动画并放大势垒右侧
        self.wait(0.5)
        
        # 放大视野
        focus_point = axes.c2p(barrier_x + barrier_width, 0, 0)
        self.play(
            self.camera.frame.animate.set_width(3).move_to(focus_point),
            run_time=2
        )
        
        # 添加标注，强调微弱波函数
        label = Text("微弱的透射波 (隧穿)", font_size=14, color=YELLOW).next_to(focus_point, UP, buff=0.5)
        arrow = Arrow(start=focus_point + RIGHT*0.5 + UP*0.5, end=focus_point + RIGHT*0.1, color=RED, stroke_width=2)
        
        self.play(Write(label), Create(arrow))
        self.wait(3)