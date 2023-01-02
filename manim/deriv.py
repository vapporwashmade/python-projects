import math

SQRT = math.sqrt(10)

from manim import *


class Deriv(MovingCameraScene):
    def construct(self):
        sideLen = ValueTracker(4)
        sideInc = ValueTracker(0)
        sep = ValueTracker(0)
        square = Square(sideLen.get_value()).set_stroke(PURE_GREEN).move_to([-3.5, 1, 0]).set_fill(GREEN_D, 1.0)
        inc1 = always_redraw(lambda : Rectangle(width=sideInc.get_value(), height=sideLen.get_value()).set_stroke(PURE_GREEN).align_to(square, UP).next_to(square, RIGHT, buff=sep.get_value()))
        inc2 = always_redraw(lambda : Rectangle(height=sideInc.get_value(), width=sideLen.get_value()).set_stroke(PURE_GREEN).align_to(square, LEFT).next_to(square, DOWN, buff=sep.get_value()))
        incSq = always_redraw(lambda : Square(sideInc.get_value()).set_stroke(PURE_GREEN).next_to(inc1, DOWN, buff=sep.get_value()).next_to(inc2, RIGHT, buff=sep.get_value()))

        texInc = MathTex(r"x \Delta x").move_to([-5, -3.5, 0])
        texSq = MathTex(r"(\Delta x)^2").move_to([-1, -3.5, 0])

        self.func()
        self.wait(2)
        self.clear()
        self.next_section()
        sideLenTex = MathTex("x").next_to(square, UP)
        sideLenTex2 = MathTex("x").next_to(square, LEFT)
        area = MathTex(r"x^2").move_to(square.get_center())
        self.play(DrawBorderThenFill(square))
        self.wait()
        self.play(Write(sideLenTex), Write(sideLenTex2))
        self.play(Write(area))
        self.wait(2)
        self.add(inc1, inc2, incSq)
        self.play(sideInc.animate.set_value(1))
        self.wait(2)
        self.next_section()
        inc1Tex = always_redraw(lambda : MathTex("\Delta x").next_to(inc1, UP))
        inc2Tex = always_redraw(lambda : MathTex("\Delta x").next_to(inc2, LEFT))
        iArrow1 = always_redraw(lambda : CurvedArrow(start_point=texInc.get_edge_center(UP).data, end_point=inc1.get_center(), angle=math.pi/5))
        iArrow2 = always_redraw(lambda : CurvedArrow(start_point=texInc.get_edge_center(UP), end_point=inc2.get_center(), angle=math.pi/5))
        iArrowSq = always_redraw(lambda : CurvedArrow(start_point=texSq.get_edge_center(UP), end_point=incSq.get_center(), angle=math.pi/5))
        self.play(Write(inc1Tex), Write(inc2Tex))
        self.wait(2)
        self.play(Write(texInc), Write(texSq))
        self.play(Create(iArrow1), Create(iArrow2), Create(iArrowSq))
        self.wait(2)
        self.next_section()
        self.play(sideInc.animate.set_value(0.1), run_time=5)
        inc1dx = always_redraw(lambda : MathTex("dx").next_to(inc1, UP))
        inc2dx = always_redraw(lambda : MathTex("dx").next_to(inc2, LEFT))
        self.play(Transform(inc1Tex, inc1dx, replace_mobject_with_target_in_scene=True), Transform(inc2Tex, inc2dx, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Transform(inc1dx, inc1Tex, replace_mobject_with_target_in_scene=True), Transform(inc2dx, inc2Tex, replace_mobject_with_target_in_scene=True))
        self.play(sideInc.animate.set_value(0.5))
        self.wait(2)
        self.play(sep.animate.set_value(1))
        self.wait(2)
        self.play(sideInc.animate.set_value(0.1), run_time=5)
        self.wait(2)

        origSquareArea = MathTex(r"x^2").shift(UP * 2, RIGHT * 1.65)
        newSquareArea = MathTex(r"+ 2x \Delta x").next_to(origSquareArea, RIGHT).align_to(origSquareArea, UP)
        diffArea = MathTex(r"+ (\Delta x)^2").next_to(newSquareArea, RIGHT).align_to(origSquareArea, UP)
        newArea = MathTex(r"-(x^2)").next_to(diffArea).align_to(origSquareArea, UP)
        unsimplified = VGroup(origSquareArea, newSquareArea, diffArea, newArea)
        simplified = VGroup(newSquareArea, diffArea)

        formula1 = MathTex(r"\frac{\Delta y}{\Delta x}").shift(RIGHT * 3)
        formula2 = MathTex(r"\frac{\Delta (x^2)}{\Delta x}").shift(RIGHT * 3)
        formula3 = MathTex(r"\frac{2x \Delta x + (\Delta x)^2}{\Delta x}").shift(RIGHT * 3)
        formula4 = MathTex(r"\frac{2x \Delta x}{\Delta x}").shift(RIGHT * 3)
        formula5 = MathTex(r"2x").shift(RIGHT * 3)

        self.play(Transform(area, origSquareArea, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Transform(VGroup(iArrow1, iArrow2, texInc), newSquareArea, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Transform(VGroup(iArrowSq, texSq), diffArea, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Write(newArea))
        self.wait(2)
        self.play(Transform(unsimplified, simplified))
        self.wait(2)
        self.play(Write(formula1))
        self.wait(2)
        self.play(TransformMatchingTex(formula1, formula2))
        self.wait(2)
        self.play(TransformMatchingTex(formula2, formula3))
        self.wait(2)
        self.play(TransformMatchingTex(formula3, formula4))
        self.wait(2)
        self.play(TransformMatchingTex(formula4, formula5))
        self.wait(2)

    def func(self):
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True, "include_tip": False},
            x_axis_config={"label_direction": DOWN},
            y_axis_config={"label_direction": LEFT}
        ).to_corner(DL)
        square_func = axes.plot(
            lambda t: t**2,
            x_range=(0, SQRT),
            color=BLUE
        )
        title = axes.get_graph_label(square_func, MathTex(f"y = x^{2}"), 3, RIGHT, 1)

        x = ValueTracker(2)
        dx = ValueTracker(1)
        x2 = x.get_value() + dx.get_value()

        bounds = always_redraw(lambda: axes.get_vertical_lines_to_graph(square_func, [x.get_value(), x.get_value() + dx.get_value()], 2))

        secant = always_redraw(lambda: axes.get_secant_slope_group(x.get_value(), square_func, dx.get_value(), secant_line_length=4))
        dx_line = secant.dx_line
        dy_line = secant.df_line
        xbrace = always_redraw(lambda : Brace(dx_line, sharpness=1, buff=0))
        xbraceText = always_redraw(lambda : MathTex("\Delta x").next_to(xbrace, DOWN, buff=0.2))
        ybrace = always_redraw(lambda : Brace(dy_line, direction=RIGHT, sharpness=1, buff=0))
        ybraceText = always_redraw(lambda : MathTex("\Delta y").next_to(ybrace, RIGHT, buff=0.2))

        secantFormula = MathTex(r"slope \ of \ secant = \frac{\Delta y}{\Delta x}").shift(RIGHT * 3)
        secantFormula2 = MathTex(r"slope \ of \ secant = \frac{change \ in \ x^2}{change \ in \ x}", font_size=40).shift(RIGHT * 3)
        secantFormula3 = MathTex(r"slope \ of \ secant = \frac{change \ in \ area \ of \ a \ square}{change \ in \ its \ side \ length}", font_size=32).shift(RIGHT * 3)

        # always_redraw(lambda: s_dot.move_to(axes.c2p(x.get_value(), square_func.underlying_function(x.get_value()))))
        # always_redraw(lambda: e_dot.move_to(
        #     axes.c2p(x.get_value() + dx.get_value(), square_func.underlying_function(x.get_value() + dx.get_value()))))

        self.play(Write(axes), Create(square_func), Write(title), subcaption_duration=2)
        self.wait(2)
        self.play(Create(bounds))
        self.wait(2)
        self.play(Create(secant))
        self.play(GrowFromCenter(xbrace), GrowFromCenter(ybrace), Write(xbraceText), Write(ybraceText))
        self.wait(2)
        self.play(Write(secantFormula))
        self.wait(2)
        self.play(dx.animate.set_value(0.001))
        xbracedx = always_redraw(lambda : MathTex("dx").next_to(xbrace, DOWN, buff=0.2))
        ybracedy = always_redraw(lambda : MathTex("dy").next_to(ybrace, RIGHT, buff=0.2))
        self.play(Transform(xbraceText, xbracedx, replace_mobject_with_target_in_scene=True), Transform(ybraceText, ybracedy, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Transform(xbracedx, xbraceText, replace_mobject_with_target_in_scene=True), Transform(ybracedy, ybraceText, replace_mobject_with_target_in_scene=True))
        self.play(dx.animate.set_value(1))
        self.wait(2)
        self.play(Transform(secantFormula, secantFormula2, replace_mobject_with_target_in_scene=True))
        self.wait(2)
        self.play(Transform(secantFormula2, secantFormula3, replace_mobject_with_target_in_scene=True))
        self.wait(2)

class OneByX(MovingCameraScene):
    def construct(self):
        x = ValueTracker(4)
        area = 12
        rect = always_redraw(lambda: Rectangle(width=x.get_value(), height=area/x.get_value()).set_stroke(PURE_RED).move_to([-5, 3, 0], UP+LEFT).set_fill(RED_C, 1.0))
        areaTex = always_redraw(lambda : MathTex(1).move_to(rect))
        xSide = always_redraw(lambda : MathTex(round(x.get_value(), 2)).next_to(rect, UP))
        otherSide = always_redraw(lambda : MathTex(round(area/x.get_value(), 2)).next_to(rect, RIGHT))

        self.play(DrawBorderThenFill(rect))
        self.play(Write(areaTex), Write(xSide), Write(otherSide))
        self.play(x.animate.set_value(1), run_time=3)
        self.wait()
        self.play(x.animate.set_value(10), run_time=3)
