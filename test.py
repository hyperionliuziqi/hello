from manim import *
import numpy as np

class QuantumTunneling(ThreeDScene):
    def construct(self):
        # ========================================
        # 第一部分：3D势阱与小球滚动 (≤10秒)
        # ========================================
        
        # 设置3D视角
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.8)
        
        # 创建3D势阱（抛物面）
        def potential_well_3d(u, v):
            x = 4 * (u - 0.5)
            y = 4 * (v - 0.5)
            z = 0.4 * (x**2 + y**2) - 1.5
            return np.array([x, y, z])
        
        well_surface = Surface(
            potential_well_3d,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(30, 30),
            fill_opacity=0.85,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5
        )
        
        # 创建3D小球
        ball_3d = Sphere(radius=0.25, color=RED, resolution=(20, 20))
        ball_3d.set_sheen(0.8, direction=UL)
        
        # 小球初始位置
        start_x = 1.5
        ball_3d.move_to([start_x, 0, 0.4 * start_x**2 - 1.5])
        
        self.add(well_surface)
        self.play(FadeIn(ball_3d), run_time=0.5)
        
        # 小球沿势阱来回滚动（不越过边缘）
        def ball_path_3d(t):
            x = 1.5 * np.cos(2 * PI * t)
            y = 0
            z = 0.4 * x**2 - 1.5
            return np.array([x, y, z])
        
        # 来回滚动两次
        self.play(
            UpdateFromAlphaFunc(
                ball_3d,
                lambda m, alpha: m.move_to(ball_path_3d(alpha))
            ),
            run_time=4.5,
            rate_func=linear
        )
        
        self.play(
            UpdateFromAlphaFunc(
                ball_3d,
                lambda m, alpha: m.move_to(ball_path_3d(1 - alpha))
            ),
            run_time=4.5,
            rate_func=linear
        )
        
        # ========================================
        # 第二部分：视角转换到2D (2秒)
        # ========================================
        
        # 使用 move_camera 方法而不是 animate
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            run_time=2
        )
        
        self.wait(0.5)
        
        # ========================================
        # 第三部分：2D势阱与小球滚动
        # ========================================
        
        # 移除3D对象
        self.play(FadeOut(well_surface), FadeOut(ball_3d), run_time=0.5)
        
        # 创建2D坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 3.5, 1],
            x_length=11,
            y_length=6,
            axis_config={"include_tip": False, "stroke_width": 2}
        )
        
        # 2D势阱曲线
        well_2d = axes.plot(
            lambda x: 0.5 * x**2,
            x_range=[-2.2, 2.2],
            color=BLUE,
            stroke_width=4
        )
        
        # 势垒（右侧）
        barrier_height = 2.5
        barrier = Line(
            start=axes.c2p(1.8, 0),
            end=axes.c2p(1.8, barrier_height),
            color=GREY,
            stroke_width=8
        )
        
        self.play(Create(axes), Create(well_2d), Create(barrier), run_time=1)
        
        # 2D小球
        ball_2d = Dot(
            point=axes.c2p(1.2, 0.5 * 1.2**2),
            radius=0.15,
            color=RED
        )
        ball_2d.set_sheen(0.5, direction=UL)
        
        self.play(FadeIn(ball_2d), run_time=0.3)
        
        # 小球在2D势阱中滚动
        def ball_path_2d(t):
            x = 1.2 * np.cos(2 * PI * t)
            y = 0.5 * x**2
            return axes.c2p(x, y)
        
        self.play(
            UpdateFromAlphaFunc(
                ball_2d,
                lambda m, alpha: m.move_to(ball_path_2d(alpha))
            ),
            run_time=3,
            rate_func=linear
        )
        
        # ========================================
        # 第四部分：小球变为概率云
        # ========================================
        
        # 创建概率云（亮度不均的粒子群）
        cloud_particles = VGroup()
        np.random.seed(42)
        
        for _ in range(200):
            # 高斯分布的位置
            x = np.random.normal(0, 0.6)
            y_base = 0.5 * x**2
            y = y_base + np.random.normal(0, 0.2)
            
            # 根据距离中心的远近设置亮度
            distance = np.sqrt(x**2 + (y - y_base)**2)
            opacity = np.exp(-distance**2 / 0.3) * 0.6
            opacity = np.clip(opacity, 0.05, 0.6)
            
            particle = Dot(
                point=axes.c2p(x, y),
                radius=0.04,
                color=BLUE_C
            ).set_opacity(opacity)
            
            cloud_particles.add(particle)
        
        self.play(
            Transform(ball_2d, cloud_particles),
            run_time=2
        )
        self.wait(1)
        
        # ========================================
        # 第五部分：概率云变为波函数
        # ========================================
        
        # 初始波包（高斯波包）
        wave_initial = axes.plot(
            lambda x: 0.8 * np.exp(-((x + 1)**2) / 0.3) * np.cos(8 * x) + 1.2,
            x_range=[-2.2, 0.5],
            color=YELLOW,
            stroke_width=3
        )
        
        self.play(
            Transform(ball_2d, wave_initial),
            run_time=2
        )
        self.wait(0.5)
        
        # ========================================
        # 第六部分：波函数传播、反射与透射
        # ========================================
        
        # 入射波（向右传播）
        incident_wave = axes.plot(
            lambda x: 0.6 * np.exp(-((x - 0.5)**2) / 0.4) * np.cos(8 * x) + 1.2,
            x_range=[-2.2, 1.7],
            color=YELLOW,
            stroke_width=3
        )
        
        # 反射波（向左，幅度较大）
        reflected_wave = axes.plot(
            lambda x: 0.4 * np.exp(-((x - 0.5)**2) / 0.4) * np.cos(8 * x) + 1.2,
            x_range=[-2.2, 1.7],
            color=ORANGE,
            stroke_width=3
        )
        
        # 透射波（穿过势垒，幅度很小）
        transmitted_wave = axes.plot(
            lambda x: 0.12 * np.exp(-((x - 2.2)**2) / 0.3) * np.cos(8 * (x - 1.8)) + 1.2,
            x_range=[1.85, 2.8],
            color=GREEN,
            stroke_width=3
        )
        
        # 波函数传播动画
        self.play(
            Transform(ball_2d, incident_wave),
            run_time=2
        )
        
        self.play(
            FadeIn(reflected_wave),
            FadeIn(transmitted_wave),
            run_time=2
        )
        
        self.wait(1)
        
        # ========================================
        # 第七部分：局部放大透射部分
        # ========================================
        
        # 创建放大框
        zoom_rect = Rectangle(
            width=2.5,
            height=2,
            color=WHITE,
            stroke_width=3
        )
        zoom_rect.move_to(axes.c2p(2.2, 1.5))
        
        self.play(Create(zoom_rect), run_time=1)
        self.wait(0.5)
        
        # 放大到透射区域
        zoom_group = VGroup(
            axes,
            well_2d,
            barrier,
            ball_2d,
            reflected_wave,
            transmitted_wave
        )
        
        self.play(
            zoom_group.animate.scale(2.5).shift(LEFT * 5 + DOWN * 2),
            zoom_rect.animate.scale(2.5).shift(LEFT * 5 + DOWN * 2),
            run_time=2.5
        )
        
        # 添加标注
        label = Text("量子隧穿", font="SimHei", font_size=28, color=GREEN)
        label.to_edge(UP)
        
        arrow = Arrow(
            start=UP * 0.5,
            end=DOWN * 0.5,
            color=GREEN,
            stroke_width=3
        ).next_to(transmitted_wave, UP, buff=0.3).shift(RIGHT * 0.5)
        
        self.add_fixed_in_frame_mobjects(label)
        self.play(
            FadeIn(label),
            GrowArrow(arrow),
            run_time=1.5
        )
        
        self.wait(3)
