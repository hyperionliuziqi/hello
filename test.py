a=1
b=2
c=3
print(f"a+b+c = {a+b+c}")
d=a*b*c
print(f"d = {d}")
from manim import *
class Test(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(Write(text))
        self.wait(2)