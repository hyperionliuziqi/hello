from manim import *
class Test(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        q=Text("Fuck you")
        self.play(Write(q))
        square = Square().shift(LEFT*2)
        triangle = Triangle().shift(RIGHT*2)
        self.play(Create(square))
        self.play(Create(triangle))
        self.wait(1)