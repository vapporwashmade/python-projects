from manim import *

class Test(Scene):
    def construct(self):
        circle = Circle()

        square = Square()
        point_center = square.get_center()
        self.add(square)
        self.play(square.animate.set_stroke(BLUE))
        self.play(square.animate.shift(UP * 2))
        self.play(square.animate.set_fill(PURE_GREEN, opacity=1.0), Rotate(square, angle=PI * 3, run_time=3))
        self.wait(2)


class Func(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 12, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": True, "include_tip": False},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).to_corner(DL)
        title = MathTex(f"y = x^{2}").shift(UP * 2, RIGHT)
        axis_labels = axes.get_axis_labels("Distance (m)", "Time (s)")

        square_func = axes.plot(
            lambda t: 10 / (1 + (t / (10 - t))**-3),
            x_range=(0, 10),
            discontinuities=[0, 10],
            color=BLUE
        )

        x = ValueTracker(3)
        dx = ValueTracker(1)
        x2 = x.get_value() + dx.get_value()

        secant = always_redraw(
            lambda: axes.get_secant_slope_group(x.get_value(), square_func, dx.get_value(), secant_line_length=4)
        )

        s_dot = Dot().set_fill(ORANGE).scale(0.8)
        e_dot = Dot().set_fill(ORANGE).scale(0.8)
        always_redraw(lambda : s_dot.move_to(axes.c2p(x.get_value(), square_func.underlying_function(x.get_value()))))
        always_redraw(lambda : e_dot.move_to(axes.c2p(x.get_value() + dx.get_value(), square_func.underlying_function(x.get_value() + dx.get_value()))))

        func_trace = VMobject()
        self.add(func_trace)
        func_trace.add_updater(lambda m: m.become(square_func.get_subcurve(x.get_value() + dx.get_value(), x2).set_stroke(PURE_RED)))

        self.play(Write(axes), Create(square_func), Write(title), subcaption_duration=2)
        self.play(Create(VGroup(s_dot, e_dot, secant)))
        self.wait()
        self.play(dx.animate.set_value(0.5))
        self.wait()
        self.play(dx.animate.set_value(0.1))
        self.wait()
        self.play(dx.animate.set_value(0.05))
        self.wait()
        self.play(dx.animate.set_value(0.01))
        self.wait()
        self.play(dx.animate.set_value(0.00001), rate_func=linear)
        self.wait(3)
class evenIter:
    def __iter__(self):
        self.val = 0
        return self

    def __next__(self):
        self.val += 2
        return self.val