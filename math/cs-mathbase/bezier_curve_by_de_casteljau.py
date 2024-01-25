from manim import *

"""

python3 math/cs-mathbase/bezier_curve_by_de_casteljau.py
manim -pql  math/cs-mathbase/bezier_curve_by_de_casteljau.py BezierCurve --disable_caching

Wiki:
 - https://en.wikipedia.org/wiki/B%C3%A9zier_curve
 - https://en.wikipedia.org/wiki/Bernstein_polynomial

"""

#config["disable_caching"] = True

THE_CODE_PATH = "math/cs-mathbase/bezier_curve_by_de_casteljau.py.png"

class BezierCurve(Scene):
    def construct(self):

        # 1.init
        self.__beizer_curve_enable = True
        self.__t = 0 # for tvalue_helper

        t = ValueTracker(0)
        control_dots = VGroup()

        # 2.Demo
        dots, numberplane = self._point_to_curve()


        # 3.De Casteljau
        video_title = Text("贝塞尔曲线(Bézier Curve) - De Casteljau算法动画").scale(0.65)
        video_title.to_corner(UP + LEFT)

        #self.play(Transform(dots, video_title)) # Note: Transform will be lead to obj invalid
        self.play(ReplacementTransform(dots, video_title))
        self.wait()

        expr1 = MathTex(
            r"f_n(p_0, ..., p_n, t)", "=" ,
            r"\begin{cases}f_{n - 1}(p_0', ..., p_{n - 1}', t), &  n > 1 \\p_0, & n = 0\end{cases}"
        )
        expr2 = MathTex(
            r"p_{n-1}' = p_{n-1} + t*\overrightarrow{p_{n-1}p_{n}}, \hspace{0.5cm} t \in [0, 1]\\"
        )
        
        self.expr = VGroup(expr1, expr2).arrange(DOWN)

        self.play(
            FadeIn(self.expr[0]),
            Write(self.expr[1], shift=DOWN)
        )

        self.wait(5)

        framebox1 = SurroundingRectangle(self.expr[0][0], buff = .1)
        framebox2 = SurroundingRectangle(self.expr[0][2], buff = .1)

        self.play(Create(framebox1))
        self.wait(5)

        self.play(ReplacementTransform(framebox1, framebox2))
        self.wait(15)

        framebox3 = SurroundingRectangle(self.expr[1], buff = .1)
        self.play(ReplacementTransform(framebox2, framebox3))

        self.wait(10)

        # 4.Animate De Casteljau
        box_and_expr = VGroup(self.expr[1], framebox3)
        self.play(
            #self.expr[0].animate.scale(0.5),
            box_and_expr.animate.scale(0.7),
        )

        self.play(
            box_and_expr.animate.shift(2 * DOWN - self.expr[1].get_center()),
            FadeOut(self.expr[0])
        )

        self.wait(10)


        # add Control Dot
        control_dots.add(
            VGroup(Dot(ORIGIN).set_color(RED)),
            VGroup(Dot([2, 2, 0]).set_color(GREEN)),
        )

        p0p1 = self._dynamic_arrow(control_dots[0], control_dots[1])

        p0_text = MathTex('P_0(0, 0)').next_to(ORIGIN, DOWN).scale(0.6)
        p1_text = MathTex('P_1(2, 2)').next_to(p0p1.get_end(), RIGHT).scale(0.6)
        p0p1_group = VGroup(p0p1, p0_text, p1_text)

        self.play(Create(p0p1_group), run_time=2)

        self.wait(6)

        # n = 1
        degree1_group = self._create_degree_helper(1)

        self.play(Create(degree1_group))

        self.expr.add(
            VGroup(
                MathTex(r"f_1'(p0, p1, t) = f_0(p_0', t) = p_0'(t)"),
                MathTex(
                    r"p_0'(t) = p_0 + t*\overrightarrow{p_{0}p_{1}}",
                    r", \hspace{0.5cm} t \in [0, 1]\\"
                )
            ).arrange(DOWN)
        )
        self.expr[2].move_to(box_and_expr.get_center())
        self.expr[2].set_color(RED)
        self.play(
            FadeOut(box_and_expr),
            FadeIn(self.expr[2])
        )

        self.wait(30)

        new_1_p0 = self._compute_new_point_and_return(p0p1, t, PURE_GREEN)

        self._wait_but_update_t(t, 4)
        self._wait_but_update_t(t, 4)
        self.play(t.animate.set_value(0.5))

        p0_text_new = MathTex('P_0(-2, 0)').next_to(LEFT * 2, DOWN).scale(0.6)

        self.play(
            ReplacementTransform(p0_text, p0_text_new),
            control_dots[0].animate.move_to(LEFT * 2),
        )

        p1_text_new = MathTex('P_1(0, 2)').next_to(UP * 2, UP).scale(0.6)
        self.play(
            ReplacementTransform(p1_text, p1_text_new),
            control_dots[1].animate.move_to(UP * 2),
        )

        # n = 2
        degree2_group = self._create_degree_helper(2)

        self.play(
            FadeOut(degree1_group),
            FadeIn(degree2_group),
        )

        control_dots.add(VGroup(Dot([3, 1, 0]).set_color(PURE_BLUE)))

        p1p2 = self._dynamic_arrow(control_dots[1], control_dots[2])

        p2_text = MathTex('P_2(3, 1)').next_to(p1p2.get_end(), RIGHT).scale(0.6)

        self.add(control_dots[2])
        self.play(Write(VGroup(p1p2, p2_text)))

        def dynamic_text():
            t_value = Text('t = {:.2f}'.format(t.get_value()))
            t_value.to_corner(RIGHT + UP).scale(0.5).set_color(PURE_RED)
            return t_value

        t_text = always_redraw(dynamic_text)

        self.expr.add(
            VGroup(
                MathTex(r"f_2'(p0, p1, p2, t) = f_1(p_0', p_1', t)"),
                MathTex(r"f_1'(p_0', p_1', t) = f_0(p_0'', t) = p_0''(t)"),
                MathTex(
                    r"p_0''(t) = p_0' + t*\overrightarrow{p_{0}'p_{1}'}"
                    r", \hspace{0.1cm} t \in [0, 1]\\"
                )
            ).arrange(DOWN)
        )

        self.expr[3].to_corner(RIGHT + DOWN)
        self.expr[3].set_color(RED).scale(0.6)

        self.play(
            ReplacementTransform(new_1_p0, t_text),
            ReplacementTransform(self.expr[2], self.expr[3])
        )

        self.wait(5)

        # point group
        new_1_p0 = self._compute_new_point_and_return(p0p1, t, PURE_RED, "p_0'")
        new_1_p1 = self._compute_new_point_and_return(p1p2, t, PURE_GREEN, "p_1'")

        self.wait(8)

        self._wait_but_update_t(t, 10)

        # sub-problem(n = 1)
        new_1_p0p1, new_2_p0 = self._create_dynamic_line_and_next_point(
            new_1_p0[0],
            new_1_p1[0],
            t
        )
        self._wait_but_update_t(t, 5)

        # Draw Beizer Curve
        self._create_dynamic_beizer_curve(control_dots)
        self.play(
            FadeIn(self.curve),
            t.animate.set_value(self._tvalue_helper())
        )

        # Move Control dot and add P3
        new_p0123 = [DOWN + LEFT * 2, UP + LEFT, UP + RIGHT, DOWN + RIGHT * 2]

        ## Move P0
        p0_text = p0_text_new
        p0_text_new = MathTex('P_0(-1, -2)').next_to(new_p0123[0], DOWN).scale(0.6)
        self.play(
            ReplacementTransform(p0_text, p0_text_new),
            control_dots[0].animate.move_to(new_p0123[0]),
            t.animate.set_value(self._tvalue_helper()),
        )

        self._wait_but_update_t(t, 2)

        ## Move P1
        p1_text = p1_text_new
        p1_text_new = MathTex('P_1(-1, 1)').next_to(new_p0123[1], UP).scale(0.6)
        self.play(
            ReplacementTransform(p1_text, p1_text_new),
            control_dots[1].animate.move_to(new_p0123[1]),
            t.animate.set_value(self._tvalue_helper()),
        )

        self._wait_but_update_t(t, 2)

        ## Move P2 And Create P3 & connect p2p3
        p2_text_new = MathTex('P_2(1, 1)').next_to(new_p0123[2], UP).scale(0.6)

        self.play(
            ReplacementTransform(p2_text, p2_text_new),
            control_dots[2].animate.move_to(new_p0123[2]),
            t.animate.set_value(self._tvalue_helper()),
        )

        ## Create P3 And Connect p2p3

        self.__beizer_curve_enable = False # need disable old-curve when add control-dot 

        # n = 3
        degree3_group = self._create_degree_helper(3)

        control_dots.add(VGroup(Dot(point=new_p0123[3]).set_color(ORANGE)))
        p2p3 = self._dynamic_arrow(control_dots[2], control_dots[3])
        p3_text = MathTex('P_3(3, 1)').next_to(
            control_dots[3].get_center(),
            RIGHT
        ).scale(0.6)

        self.play(
            Create(control_dots[3]),
            Create(VGroup(p2p3, p3_text)),
            FadeOut(self.expr[3]),
            FadeOut(degree2_group),
            FadeIn(degree3_group),
            t.animate.set_value(0.5),
        )

        new_1_p2 = self._compute_new_point_and_return(p2p3, t, BLUE, "p_2'")
        self.play(t.animate.set_value(self._tvalue_helper()))
        new_1_p1p2, new_2_p1 = self._create_dynamic_line_and_next_point(new_1_p1[0], new_1_p2[0], t)
        self.play(t.animate.set_value(self._tvalue_helper()))
        new_2_p0p1, new_3_p0 = self._create_dynamic_line_and_next_point(
            new_2_p0[0], new_2_p1[0],
            t, level=0.7, point_color=PINK
        )
        self.play(t.animate.set_value(self._tvalue_helper()))
        self.play(t.animate.set_value(0.5))

        # Formula
        details_control = VGroup(
            VGroup(new_1_p0, new_1_p1, new_1_p2, new_1_p0p1, new_1_p1p2),
            VGroup(new_2_p0, new_2_p1, new_2_p0p1),
            VGroup(new_3_p0)
        )

        self.expr.add(MathTex(
            r"f_n(P_0, ..., P_n, t) = \begin{cases}f_{n - 1}(P_0', ..., P_{n - 1}', t), &  n > 1 \\P_0, & n = 0\end{cases}",
            r"P_{n-1}' = P_{n-1} + t*\overrightarrow{P_{n-1}P_{n}}, \hspace{0.1cm} t \in [0, 1]\\",
            r"P_{n-1}' = (1-t)P_{n-1} + tP_n, \hspace{0.1cm} t \in [0, 1]\\",
        ).arrange(DOWN))

        self.expr[4].move_to([4, 2, 0]).scale(0.4)

        expr4_background = SurroundingRectangle(self.expr[4])
        expr4_background.set_color(BLUE).set_fill("#F0E68C", opacity=0.15)

        self.play(
            Create(expr4_background),
            FadeIn(self.expr[4]),
            FadeOut(details_control),
        )

        self.wait(2)

        formula1_group = VGroup(
            Dot().set_color(PURE_RED), MathTex(r"P_0' = (1-t)P_0 + tP_1").scale(0.5),
            Dot().set_color(PURE_GREEN), MathTex(r"P_1' = (1-t)P_1 + tP_2").scale(0.5),
            Dot().set_color(BLUE), MathTex(r"P_2' = (1-t)P_2 + tP_3").scale(0.5),
        ).arrange(buff=0.5, direction=RIGHT)

        formula1_group.move_to(2.5 * DOWN)

        self.play(
            Write(formula1_group),
            FadeIn(details_control[0])
        )

        self.wait(3)

        formula2_group = VGroup(
            Dot().set_color(ORANGE),
            MathTex(r"P_0'' = (1-t)P_0' + tP_1' = (1-t)^2P_0 + 2t(1-t)P_1 + t^2P_2").scale(0.4),
            # ...
            Dot().set_color(ORANGE),
            MathTex(r"P_1'' = (1-t)P_1' + tP_2' = (1-t)^2P_1 + 2t(1-t)P_2 + t^2P_3").scale(0.4),
        ).arrange(buff=0.5, direction=RIGHT).move_to(2.5 * DOWN)

        self.play(
            ReplacementTransform(formula1_group , formula2_group),
            FadeIn(details_control[1])
        )

        self.wait(3)

        formula3_group = VGroup(
            Dot().set_color(PURPLE),
            MathTex(
                r"P_0^3 = (1-t)P_0'' + tP_1''",
                r" = (1-t)^3P_0 + 3t(1-t)^2P_1 + 3t^2(1-t)P_2 + t^3P_3"
            ).scale(0.5),
        ).arrange(buff=0.5, direction=RIGHT).move_to(2.5 * DOWN)

        self.play(
            ReplacementTransform(formula2_group , formula3_group),
            FadeIn(details_control[2])
        )

        self._wait_but_update_t(t, 5)
        self.__beizer_curve_enable = True
        self._wait_but_update_t(t, 5)

        # Move Control-Dot And Update Formula
        dynamic_f_pos = 2.5 * DOWN
        def dynamic_formula():
            # use text avoid re-compile latex-formula
            f = VGroup(
                MathTex(r"P^3(t)"),
                Text(" = ").scale(0.7),
                MathTex(r"(1-t)^3P_0"),
                Text("({:.2f}, {:.2f}) +".format(
                    control_dots[0].get_center()[0],
                    control_dots[0].get_center()[1])
                ).scale(0.7),
                MathTex(r"3t(1-t)^2P_1"),
                Text("({:.2f}, {:.2f}) +".format(
                    control_dots[1].get_center()[0],
                    control_dots[1].get_center()[1])
                ).scale(0.7),
                MathTex(r"3t^2(1-t)P_2"),
                Text("({:.2f}, {:.2f}) +".format(
                    control_dots[2].get_center()[0],
                    control_dots[2].get_center()[1])
                ).scale(0.7),
                MathTex(r"t^3P_3"),
                Text("({:.2f}, {:.2f})".format(
                    control_dots[3].get_center()[0],
                    control_dots[3].get_center()[1])
                ).scale(0.7),
            ).arrange(RIGHT)
            f.move_to(dynamic_f_pos)
            f.scale(0.5)
            return f

        dynamic_f = always_redraw(dynamic_formula)

        self.play(
            ReplacementTransform(formula3_group , dynamic_f),
            t.animate.set_value(self._tvalue_helper())
        )

        self._wait_but_update_t(t, 5)

        # Adjust Curve by Control Dot
        self.play(
            t.animate.set_value(self._tvalue_helper()),
            control_dots[0].animate.shift(DL)
        )
        self.play(
            t.animate.set_value(self._tvalue_helper()),
            control_dots[2].animate.shift(UP)
        )

        self._wait_but_update_t(t, 5)

        self.play(
            t.animate.set_value(self._tvalue_helper()),
            control_dots[1].animate.shift(LEFT * 2)
        )
        self.play(
            t.animate.set_value(self._tvalue_helper()),
            control_dots[1].animate.shift(RIGHT)
        )

        #self.play(t.animate.set_value(self._tvalue_helper()))

        # N-BezierCuver
        self.play(
            t.animate.set_value(self._tvalue_helper()),
            FadeOut(VGroup(p0_text_new, p1_text_new, p2_text_new, p3_text, degree3_group)),
            control_dots.animate.move_to([3.5, -1, 0])
        )

        formula4_group = VGroup(
            MathTex(
                r"[(1 - t) + t]^3 =",
                r"(1-t)^3 + 3t(1-t)^2 + 3t^2(1-t)+ t^3"
            ).scale(1.1),
            VGroup(
                MathTex(r"P_0^3 = \sum_{i=0}^{3} C_3^i (1-t)^{3-i} t^{i} P_{i}"),
                MathTex(
                    r"P(t) = P_0^n(t) = \sum_{i=0}^{n}",
                    r"C_n^i(1-t)^{n-i}", r"t^{i} P_{i}"
                )
            ).arrange(RIGHT, buff=0.5),
            VGroup(
                MathTex(r"B(t) = \sum_{i=0}^{n}", r"B_{i, n}(t)", r"P_{i}"),
                MathTex(r"B_{i, n}(t)={n \choose i}t^i(1 -t)^{n-i}"),
                MathTex(r"t \in [0, 1]")
            ).arrange(RIGHT, buff=0.5),
        ).arrange(buff=0.5, direction=DOWN)

        formula4_group.scale(0.5)
        formula4_group.move_to(3 * LEFT)

        self.play(
            t.animate.set_value(self._tvalue_helper()),
            FadeIn(formula4_group[0][1])
        )

        self._wait_but_update_t(t, 10)

        self.play(
            t.animate.set_value(self._tvalue_helper()),
            Write(formula4_group[0][0])
        )

        self._wait_but_update_t(t, 5)

        self.play( # Cube
            t.animate.set_value(self._tvalue_helper()),
            FadeIn(formula4_group[1][0])
        )

        self._wait_but_update_t(t, 5)

        self.play( # N
            t.animate.set_value(self._tvalue_helper()),
            FadeIn(formula4_group[1][1])
        )

        self._wait_but_update_t(t, 5)

        self.play(
            t.animate.set_value(self._tvalue_helper()),
            FadeIn(formula4_group[2])
        )

        self._wait_but_update_t(t, 5)

        highlight_box1 = SurroundingRectangle(formula4_group[1][1][1]).set_opacity(0.4)
        self.play( # Bernstein basis polynomials
            t.animate.set_value(self._tvalue_helper()),
            Create(highlight_box1)
        )

        self._wait_but_update_t(t, 5)

        highlight_box2 = SurroundingRectangle(formula4_group[2][0][1]).set_opacity(0.4)
        self.play( # Bernstein basis polynomials
            t.animate.set_value(self._tvalue_helper()),
            ReplacementTransform(highlight_box1, highlight_box2)
        )

        self._wait_but_update_t(t, 5)

        highlight_box3 = SurroundingRectangle(formula4_group[2][1]).set_opacity(0.4)
        self.play( # Bernstein basis polynomials
            t.animate.set_value(self._tvalue_helper()),
            ReplacementTransform(highlight_box2, highlight_box3)
        )

        # Code Implement
        code = self._code_impl()
        self.play(
            t.animate.set_value(self._tvalue_helper()),
            ReplacementTransform(highlight_box3, code)
        )

        self._wait_but_update_t(t, 20)

        # Happy Ending
        my_open_source = VGroup(
            Text("My OpenSource Homepage", t2c={"OpenSource": PURE_GREEN}),
            Text("https://github.com/Sunrisepeak", t2c={"Sunrisepeak": BLUE}).scale(0.9)
        ).arrange(DOWN).set_opacity(0.8).scale(0.8)

        t_text.clear_updaters()

        end_obj_group1 = VGroup(
            video_title, t_text, expr4_background, self.expr[4],
            formula4_group, code
        )

        self.play(
            ReplacementTransform(end_obj_group1, my_open_source[0]),
            t.animate.set_value(self._tvalue_helper())
        )

        dynamic_f.clear_updaters()

        end_obj_group2 = VGroup(
            details_control,
            self.curve, p0p1, p1p2, p2p3, control_dots
        )

        self.play(
            ReplacementTransform(dynamic_f, my_open_source[1]),
            t.animate.set_value(0.5),
            FadeOut(end_obj_group2)
        )

        self.play(
            ApplyMethod(my_open_source.set_opacity, 0.3),
            FadeOut(numberplane),
            run_time=3
        )

        self._ending_by_the_code()


    def _dynamic_arrow(self, start_control_dot, end_control_dot):

        def draw_arrow():
            arrow = Arrow(
                start_control_dot[0].get_center(), end_control_dot[0].get_center(),
                max_tip_length_to_length_ratio=0.07,
                buff=0
            ).set_stroke(width=3, opacity=0.6)
            return arrow

        return always_redraw(draw_arrow)

    def _create_dynamic_beizer_curve(self, control_dots):

        def de_casteljau(points, t):
            assert len(points) > 0
            if len(points) == 1:
                return points[0]
            else:
                new_points = []
                for i in range(len(points) - 1):
                    vec = points[i + 1] - points[i]
                    new_point = points[i] + t * vec
                    #new_point = (1 - t) * points[i] + t * points[i + 1]
                    new_points.append(new_point)
                # len(new_points) = len(points) - 1
                return de_casteljau(new_points, t)

        t_values = np.linspace(0, 1, 50) # t[0 ~ 1]

        def draw_curve():
            control_points = [d[0].get_center() for d in control_dots]
            curve_points = [de_casteljau(control_points, t) for t in t_values]
            curve = VGroup()
            last_line = Line(curve_points[0], curve_points[0]).set_opacity(0)
            if self.__beizer_curve_enable:
                for point in curve_points:
                    new_line = Line(last_line.get_end(), point)
                    new_line.set_stroke(width=4, color=PINK, opacity=0.8)
                    curve.add(new_line)
                    last_line = new_line
            return curve

        self.curve = always_redraw(draw_curve)

    def _create_dynamic_line_and_next_point(self, p0, p1, t, level=1, point_color=ORANGE):

        line = always_redraw(lambda: Line(p0, p1).set_stroke(
            width=4 * level, color=TEAL, opacity=0.5 + (1 - level)
        ))

        p = self._compute_new_point_and_return(
            line, t, point_color,
            dot_text="disable", scale_control=level
        )

        self.add(line)

        return line, p

    def _create_degree_helper(self, n):
        degree = Text("n = {}".format(n), color=RED)
        degree_box = SurroundingRectangle(degree).set_stroke(width=2, color=YELLOW_D)
        degree_group = VGroup(degree, degree_box)
        degree_group.to_corner(UP * 2.5 + LEFT).scale(0.8)

        return degree

    def _point_to_curve(self):

        tile = Text("贝塞尔曲线(Bézier Curve) 动画").scale(0.75).to_edge(UP)
        self.play(Write(tile))

        numberplane = NumberPlane()
        self.play(Create(numberplane))

        self.wait(4) #time-point 1

        d1 = Dot(point=DOWN + LEFT * 2).set_color(RED)
        d2 = Dot(point=UP + LEFT).set_color(GREEN)
        d3 = Dot(point=UP + RIGHT).set_color(BLUE)
        d4 = Dot(point=DOWN + RIGHT * 2).set_color(YELLOW)

        self.play(Create(VGroup(d1, d2, d3, d4)))

        self.wait(3) #time-point 2

        def draw_curve():
            bezier = CubicBezier(
                d1.get_center(), d2.get_center(),
                d3.get_center(), d4.get_center()
            )
            bezier.set_color(PINK)
            return bezier

        bezier = always_redraw(draw_curve)

        self.play(Create(bezier))

        self.wait(4) #time-point 3

        self.play(d1.animate.shift(DL), run_time=2)
        self.wait(3) #time-point 4-1
        self.play(d3.animate.shift(UP), run_time=2)
        self.wait(3) #time-point 4-2


        l1 = always_redraw(lambda: Line(
                d1.get_center(), d2.get_center()
            ).set_stroke(width=2, color=GRAY)
        )
        l2 = always_redraw(lambda: Line(
                d3.get_center(), d4.get_center()
            ).set_stroke(width=2, color=GRAY)
        ) 

        #time-point 5
        self.play(Create(l1), run_time=3)
        self.play(Create(l2),  run_time=2)
        self.wait(3)

        #time-point 6
        self.play(d2.animate.shift(LEFT * 2), run_time=3)
        self.play(d2.animate.shift(RIGHT), run_time=2)
        self.wait(5)

        self.play(Uncreate(VGroup(tile, l1, l2, bezier)))
        self.play(Uncreate(bezier), run_time=2)

        return VGroup(d1, d2, d3, d4), numberplane

    def _compute_new_point_and_return(self, arrow, t, color, dot_text = None, scale_control = 1):

        def draw_point():
            p = arrow.get_start() + arrow.get_vector() * t.get_value()
            dot = Dot(p).set_color(color)

            #dot.scale(scale_control * 0.8)

            if dot_text:
                if dot_text == "disable":
                    return dot
                dot_value = VGroup(
                    MathTex(dot_text),
                    Text('({:.2f},{:.2f})'.format(p[0], p[1])).scale(0.5)
                ).arrange(RIGHT).next_to(dot.get_center(), UP * 0.5 * scale_control)
            else:
                dot_value = Text('t = {:.2f}'.format(t.get_value()))
                dot_value.next_to(dot.get_center(), UP * 0.5 * scale_control).scale(0.5)

            dot_value.scale(0.6).set_color(color)

            return VGroup(dot, dot_value)

        new_p = always_redraw(draw_point)

        self.add(new_p)

        return new_p
    
    # t [0, 1]
    def _tvalue_helper(self):
        if self.__t == 0:
            self.__t = 1
        else:
            self.__t = 0

        return self.__t


    def _code_impl(self):

        code = """
def bezier_curve_de_casteljau(points, t):
    assert len(points) > 0
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            vec = points[i + 1] - points[i]
            new_point = points[i] + t * vec
            #new_point = (1 - t) * points[i] + t * points[i + 1]
            new_points.append(new_point)
        # len(new_points) = len(points) - 1
        return bezier_curve_de_casteljau(new_points, t)
"""

        rendered_code = Code(
            code=code, tab_width=4, background="window",
            language="Python", font="Monospace", style="emacs"
        )
        rendered_code.scale(0.6)
        rendered_code.set_opacity(0.8)
        
        return rendered_code

    def _wait_but_update_t(self, t, run_time_s=1):
        for i in range(0, run_time_s):
            self.play(t.animate.set_value(self._tvalue_helper()))

    def _ending_by_the_code(self):

        print("Happy Ending!")

        return

        code = ImageMobject(THE_CODE_PATH)

        code.get_top()

        self.play(code.animate.shift(code.get_top()), run_time=3)

if __name__ == "__main__":
    scene = BezierCurve()
    scene.render()