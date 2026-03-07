from manim import *
import numpy as np
import random

class ComplexMathAnimation(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 第一部分：3D坐标轴和复杂函数
        self.show_complex_function()
        
        # 第二部分：傅里叶级数可视化
        self.show_fourier_series()
        
        # 第三部分：分形几何
        self.show_fractal()
        
        # 第四部分：粒子系统模拟
        self.show_particle_system()
        
        # 结尾
        self.show_ending()
    
    def show_complex_function(self):
        # 清除之前的对象
        self.clear()
        
        # 创建3D坐标轴
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=8,
            y_length=8,
            z_length=6
        )
        axes.add(axes.get_axis_labels())
        
        # 标题
        title = Text("复变函数可视化", font_size=36, color=BLUE)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # 创建复平面上的网格
        complex_plane = NumberPlane(
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).scale(1.5)
        
        # 创建复杂的函数表面 f(z) = z^2
        def func(u, v):
            z = complex(u, v)
            w = z**2
            return np.array([u, v, w.real])
        
        surface = Surface(
            func,
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(32, 32),
            fill_opacity=0.7,
            stroke_width=0.5,
            stroke_color=WHITE,
        )
        
        # 添加渐变颜色
        surface.set_fill_by_value(axes=axes, colors=[(BLUE, -2), (PURPLE, 0), (RED, 2)])
        
        # 添加一些点来标记特殊位置
        points = VGroup()
        colors = [RED, YELLOW, GREEN, ORANGE]
        positions = [complex(1, 1), complex(-1, -1), complex(1, -1), complex(-1, 1)]
        
        for i, z in enumerate(positions):
            point = Dot3D(
                point=[z.real, z.imag, (z**2).real],
                radius=0.1,
                color=colors[i]
            )
            points.add(point)
        
        # 动画序列
        self.play(
            Create(axes),
            Create(complex_plane),
            run_time=2
        )
        self.wait(0.5)
        
        self.play(
            Create(surface),
            run_time=3
        )
        self.play(
            Create(points),
            run_time=1
        )
        
        # 旋转视角
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(1)
        
        # 清除场景
        self.play(
            *[FadeOut(mob) for mob in [axes, complex_plane, surface, points]],
            run_time=1
        )
    
    def show_fourier_series(self):
        self.clear()
        
        # 标题
        title = Text("傅里叶级数可视化", font_size=36, color=YELLOW)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        axes.center()
        
        # 标签
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 创建多个傅里叶级数的近似
        colors = [BLUE, GREEN, YELLOW, ORANGE, RED]
        n_terms = [1, 3, 5, 10, 20]
        
        # 方波的傅里叶级数
        def square_wave_approx(x, n):
            result = 0
            for k in range(1, n+1, 2):
                result += (4/(k*PI)) * np.sin(k*x)
            return result
        
        # 创建动画：逐渐添加更多项
        self.play(
            Create(axes),
            Write(axes_labels),
            run_time=2
        )
        
        current_graph = None
        for i, n in enumerate(n_terms):
            graph = axes.plot(
                lambda x: square_wave_approx(x, n),
                x_range=[0, 2*PI],
                color=colors[i % len(colors)],
                stroke_width=3 - i*0.3
            )
            
            if current_graph:
                self.play(
                    Transform(current_graph, graph),
                    run_time=1.5
                )
            else:
                self.play(
                    Create(graph),
                    run_time=2
                )
                current_graph = graph
            
            # 显示当前项数
            terms_text = Text(f"项数: {n}", font_size=24, color=WHITE)
            terms_text.next_to(title, DOWN, buff=0.5)
            
            if i == 0:
                self.add_fixed_in_frame_mobjects(terms_text)
                terms_text_old = terms_text
            else:
                self.play(
                    FadeOut(terms_text_old),
                    FadeIn(terms_text)
                )
                terms_text_old = terms_text
            
            self.wait(0.5)
        
        self.wait(2)
        
        # 清除场景
        self.play(
            *[FadeOut(mob) for mob in [axes, axes_labels, current_graph, terms_text_old]],
            run_time=1
        )
    
    def show_fractal(self):
        self.clear()
        
        # 标题
        title = Text("分形几何 - 朱莉娅集", font_size=36, color=PURPLE)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # 创建朱莉娅集
        julia_set = self.create_julia_set()
        
        # 创建一些运动的粒子
        particles = VGroup()
        num_particles = 30
        
        # 动画
        self.play(
            Create(julia_set, run_time=3)
        )
        
        # 创建并动画粒子
        for i in range(num_particles):
            dot = Dot(
                point=self.get_random_point_in_julia(),
                color=random_bright_color(),
                radius=0.03
            )
            particles.add(dot)
            self.add(dot)
            self.wait(0.05)
        
        # 粒子旋转动画
        self.play(
            Rotate(particles, angle=2*PI, about_point=ORIGIN),
            run_time=4,
            rate_func=linear
        )
        
        self.wait(2)
        
        # 清除场景
        self.play(
            *[FadeOut(mob) for mob in [julia_set, particles]],
            run_time=1
        )
    
    def show_particle_system(self):
        self.clear()
        
        # 标题
        title = Text("粒子系统模拟", font_size=36, color=GREEN)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # 创建粒子系统
        particles = VGroup()
        num_particles = 50
        
        # 创建中心球体
        center_sphere = Sphere(radius=0.5)
        center_sphere.set_color_by_gradient(BLUE, PURPLE)
        center_sphere.set_opacity(0.3)
        
        self.play(Create(center_sphere), run_time=1)
        
        # 创建粒子
        for i in range(num_particles):
            dot = Dot3D(
                point=self.get_random_point_in_sphere(),
                color=random_bright_color(),
                radius=0.05
            )
            particles.add(dot)
            self.add(dot)
            if i % 10 == 0:
                self.wait(0.1)
        
        # 粒子运动动画
        self.particle_animation(particles, center_sphere, duration=8)
        
        # 清除场景
        self.play(
            *[FadeOut(mob) for mob in [center_sphere, particles]],
            run_time=1
        )
    
    def particle_animation(self, particles, center_sphere, duration=8):
        """创建粒子运动动画"""
        velocities = []
        for particle in particles:
            # 为每个粒子创建随机速度
            vel = np.random.randn(3) * 0.05
            velocities.append(vel)
        
        def update_particles(group, dt):
            for i, particle in enumerate(group):
                current_pos = particle.get_center()
                
                # 更新位置
                new_pos = current_pos + velocities[i]
                
                # 边界检查 - 保持在球体内
                distance = np.linalg.norm(new_pos)
                if distance > 2.5:
                    # 反弹
                    velocities[i] = -velocities[i] * 0.8
                    new_pos = current_pos
                
                particle.move_to(new_pos)
        
        particles.add_updater(update_particles)
        self.wait(duration)
        particles.remove_updater(update_particles)
    
    def show_ending(self):
        self.clear()
        
        # 创建最终文字
        title = Text("数学之美", font_size=72, color=BLUE)
        subtitle = Text("Manim 复杂动画演示", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        # 添加一些装饰性的数学符号
        symbols = VGroup()
        math_symbols = ["∫", "∑", "∏", "∞", "√", "π", "e", "i"]
        for i, symbol in enumerate(math_symbols):
            sym = Text(symbol, font_size=48)
            sym.set_color_by_gradient(random_bright_color(), random_bright_color())
            angle = i * 2 * PI / len(math_symbols)
            radius = 3
            sym.move_to(radius * np.array([np.cos(angle), np.sin(angle), 0]))
            symbols.add(sym)
        
        # 动画
        self.play(
            *[Write(sym) for sym in symbols],
            run_time=2
        )
        
        self.play(
            Write(title),
            run_time=2
        )
        
        self.play(
            Write(subtitle),
            run_time=1
        )
        
        # 旋转符号
        self.play(
            Rotate(symbols, angle=2*PI, about_point=ORIGIN),
            run_time=4,
            rate_func=linear
        )
        
        # 淡出
        self.play(
            *[FadeOut(mob) for mob in [title, subtitle, symbols]],
            run_time=2
        )
    
    def create_julia_set(self, width=8, height=8, max_iter=50):
        """创建朱莉娅集"""
        c = complex(-0.7, 0.27)
        
        # 创建网格
        julia = VGroup()
        resolution = 80  # 降低分辨率以提高性能
        
        for i in range(resolution):
            for j in range(resolution):
                # 映射到复平面
                x = -2 + 4 * i / resolution
                y = -2 + 4 * j / resolution
                
                z = complex(x, y)
                n = 0
                
                # 迭代
                while n < max_iter and abs(z) <= 2:
                    z = z*z + c
                    n += 1
                
                # 根据迭代次数着色
                if n < max_iter:
                    # 使用更简单的颜色方案
                    intensity = n / max_iter
                    color = rgb_to_color([intensity, intensity*0.5, 1-intensity])
                    
                    dot = Dot(
                        point=[x * width/4, y * height/4, 0],
                        color=color,
                        radius=0.01
                    )
                    julia.add(dot)
        
        return julia
    
    def get_random_point_in_julia(self):
        """获取朱莉娅集中的随机点"""
        x = np.random.uniform(-2, 2)
        y = np.random.uniform(-2, 2)
        return np.array([x, y, 0])
    
    def get_random_point_in_sphere(self, radius=2.5):
        """获取球体内的随机点"""
        # 使用球坐标生成随机点
        theta = 2 * np.pi * np.random.random()
        phi = np.arccos(2 * np.random.random() - 1)
        r = radius * np.random.random() ** (1/3)  # 使分布更均匀
        
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        
        return np.array([x, y, z])

# 运行此文件的代码
if __name__ == "__main__":
    # 配置和运行场景
    scene = ComplexMathAnimation()
    scene.render()