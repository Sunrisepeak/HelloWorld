from manim import *

class CSMathBaseLogo(Scene):
    def construct(self):
        start_logo, title = self._start_logo()
        my_open_source = self._end_logo()
        self.play(ReplacementTransform(start_logo, my_open_source[0]))
        self.play(ReplacementTransform(title, my_open_source[1]))
        self.play(FadeOut(my_open_source), run_time=2)

    def _end_logo(self, old_objs=VGroup()):

        my_open_source = VGroup(
            Text("Welcome to My OpenSource Homepage", t2c={"OpenSource": PURE_GREEN}).scale(0.9),
            Text("https://github.com/Sunrisepeak", t2c={"Sunrisepeak": BLUE})
        ).arrange(DOWN).scale(0.8)

        return my_open_source

    def _start_logo(self):

        title = VGroup(Text("CS").scale(1.5), Text("*"), Text("Math").scale(1.3), Text("Base").scale(1.5))
        title.arrange(RIGHT, buff=0.3)
        title.move_to(DOWN)
        title[2].shift(0.2 * DOWN)
        title[1].set_color(YELLOW)
        title[3].set_color(BLUE)

        control_dots = VGroup( # P0/P1/P2/P3
            Dot(point=LEFT * 2).set_color(RED),
            Dot(point=2 * UP  + LEFT).set_color(GREEN),
            Dot(point=2 * UP + RIGHT).set_color(BLUE),
            Dot(point=RIGHT * 2).set_color(YELLOW),
        )

        self.play(Create(control_dots))

        t = ValueTracker(0)

        l0, p0_1 = self._create_dynamic_line_and_next_point(control_dots[0], control_dots[1], t, point_color=ORANGE)
        l1, p1_1 = self._create_dynamic_line_and_next_point(control_dots[1], control_dots[2], t, point_color=ORANGE)
        l2, p2_1 = self._create_dynamic_line_and_next_point(control_dots[2], control_dots[3], t, point_color=ORANGE)

        layer1 = VGroup(l0, p0_1, l1, p1_1, l2, p2_1)

        self.add(layer1)
        self.play(
            Write(title[0]),
            t.animate.set_value(1)
        )

        l0_1, p0_2 = self._create_dynamic_line_and_next_point(p0_1, p1_1, t, point_color=PURE_GREEN, line_color=PURE_BLUE)
        l1_1, p1_2 = self._create_dynamic_line_and_next_point(p1_1, p2_1, t, point_color=PURE_GREEN, line_color=PURE_BLUE)

        layer2 = VGroup(l0_1, p0_2, l1_1, p1_2)

        self.add(layer2)
        self.play(
            Write(title[1]),
            t.animate.set_value(0)
        )

        l0_2, p0_3 = self._create_dynamic_line_and_next_point(p0_2, p1_2, t, point_color=PINK, line_color=PURE_RED)

        layer3 = VGroup(l0_2, p0_3)

        self.add(layer3)
        self.play(
            Write(title[2]),
            t.animate.set_value(1)
        )

        # Details-Impl: math/cs-mathbase/bezier_curve_by_de_casteljau.py
        bezier = CubicBezier(
            control_dots[0].get_center(),
            control_dots[1].get_center(),
            control_dots[2].get_center(),
            control_dots[3].get_center()
        ).set_color(PINK).set_stroke(width=2)

        self.play(
            Write(title[3]),
            t.animate.set_value(0)
        )

        self.play(
            ApplyMethod(title[0].set_color, PURE_RED),
            Create(bezier), t.animate.set_value(1)
        )
        self.play(
            ApplyMethod(title[2].set_color, PURE_GREEN),
            t.animate.set_value(0.5)
        )

        return VGroup(control_dots, layer1, layer2, layer3, bezier), title

    def _create_dynamic_line_and_next_point(self, p0, p1, t, level=1, point_color=ORANGE, line_color=TEAL):

        line = always_redraw(lambda: Line(p0.get_center(), p1.get_center()).set_stroke(
            width=4 * level, color=line_color, opacity=0.5 + (1 - level)
        ))

        p = self._compute_new_point_and_return(line, t, point_color)

        return line, p

    def _compute_new_point_and_return(self, arrow, t, color):

        def draw_point():
            p = arrow.get_start() + arrow.get_vector() * t.get_value()
            dot = Dot(p).set_color(color)
            return dot

        new_p = always_redraw(draw_point)

        return new_p

if __name__ == "__main__":
    scene = CSMathBaseLogo()
    scene.render()