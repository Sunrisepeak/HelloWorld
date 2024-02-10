from manim import *
from logo import CSMathBase

"""

Wiki: https://zh.wikipedia.org/zh-cn/%E7%89%9B%E9%A1%BF%E6%B3%95

python3 math/cs-mathbase/funtion_zeros.py

"""

class Newton(CSMathBase):
    def construct(self):
        start_logo, start_logo_title = self._start_logo()

        pre_title = VGroup(
            Text("[近似计算]").set_color(PURE_RED),
            Text("牛顿迭代法 _ 求解函数零点", t2c={"牛顿迭代法": GREEN, "求解函数零点": BLUE})
        ).arrange(DOWN, buff=0.5).scale(1.3)

        self.play(ReplacementTransform(VGroup(start_logo, start_logo_title), pre_title))

        self.wait()

        title =  Text("求解根号2 - 牛顿迭代法").scale(1.2)
        title.set_color(YELLOW)
        title.to_corner(UP)

        self.play(ReplacementTransform(pre_title, title))

        formual1 = VGroup(
            MathTex("\sqrt{2}"),
            Text("="),
            Text("?").set_color(PURE_RED)
        ).arrange(RIGHT, buff=0.5).scale(3)

        self.play(Write(formual1))

        self.wait()

        result = Text("X").scale(3).set_color(PURE_RED)
        result.move_to(formual1[2].get_center())
        self.play(ReplacementTransform(formual1[2], result))

        self.wait()

        formual2 = VGroup(
            MathTex("2"),
            Text("="),
            MathTex("X^2").set_color(PURE_RED)
        ).arrange(RIGHT, buff=0.5).scale(3)

        self.play(ReplacementTransform(formual1, formual2))

        self.wait()

        formual3 = MathTex("f(x) = ", "x^2", "- 2").scale(3)
        formual3[1].set_color(PURE_RED)

        self.play(ReplacementTransform(formual2, formual3))

        self.wait()

        axes = Axes(
            x_range=[-2, 5],
            y_range=[-4, 25],
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-2, 5.01, 2),
                "numbers_with_elongated_ticks": np.arange(-2, 5.01, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(-4, 25, 4),
                "numbers_with_elongated_ticks": np.arange(-4, 25, 4),
            },
            tips=False,
        ).scale(0.6)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x) = x^2 - 2")
        func_graph = axes.plot(lambda x: x * x - 2, x_range=[-2, 5], color=BLUE).set_stroke(width=2)
        x0_line = axes.get_vertical_line(axes.input_to_graph_point(4, func_graph), color=YELLOW)

        graph = VGroup(axes, axes_labels.scale(0.7), func_graph, x0_line)

        formual4 = MathTex(
            "f(x) = f(x_0) + f'(x_0)(x - x_0)", "+ f''(x_0)(x - x_0)^2 + ...")

        formual4.move_to(2.5 * DOWN)

        self.play(
            Create(graph),
            ReplacementTransform(formual3, formual4)
        )

        self.wait()

        formual4_box = SurroundingRectangle(formual4[0])

        self.play(
            Create(formual4_box),
            FadeOut(formual4[1])
        )

        self.wait()

        self.play(graph.animate.to_corner(LEFT))

        Xs = VGroup(
            MathTex("X_0 = 4.00"),
            MathTex("X_1 = 2.25"),
            MathTex("X_2 = {:.2f}".format(self.nweton_sqrt_next(2.25))),
            MathTex("X_3 = {:.2f}".format(self.nweton_sqrt_next(
                    self.nweton_sqrt_next(2.25)
                ))
            )
        ).arrange(DOWN, buff=0.2).to_corner(1.5 * RIGHT)

        x0_dot = Dot(axes.coords_to_point(4, 0), color=PINK)
        self.play(Create(x0_dot))
        self.play(ReplacementTransform(x0_dot, Xs[0]))

        self.wait()

        x1, x1_dot = self._next_draw(graph, 4)

        self.wait()

        self.play(ReplacementTransform(x1_dot, Xs[1]))

        self.wait()

        x2, x2_dot = self._next_draw(graph, x1)

        self.wait()

        self.play(ReplacementTransform(x2_dot, Xs[2]))

        self.wait()

        self.camera.frame.save_state()

        x3, x3_dot = self._next_draw(graph, x2)

        self.wait()

        self.play(self.camera.frame.animate.scale(0.2).move_to(x3_dot))

        self.wait()

        self.play(
            ReplacementTransform(x3_dot, Xs[3]),
            Restore(self.camera.frame)
        )

        self.wait()

        formual5 = VGroup(
            MathTex(r"X_{n+1} = X_n - \frac{f(X_n)}{f'(X_n)}", r", f'(x) != 0"),
            Text("其中x属于[a-r, a+r], a为零点, r为X0到a的距离").scale(0.7),
            Text("算法复杂度通常优于二分法(logN)").scale(0.7)
        ).arrange(DOWN, buff=0.5).scale(0.6).to_corner(RIGHT)

        self.play(ReplacementTransform(Xs, formual5))

        self.wait()

        code = """
# 计算平方根: f(x) = x^2 - a
def sqrt_newton(target, tolerance=0.0001):

    Xn = target # 牛顿迭代法的初始估计值

    while True:
        # 计算新的估计值 Xn+1 = Xn - F(Xn) / F'(Xn)
        new_Xn = Xn - (Xn * Xn - target) / (2 * Xn)

        # 检查新的估计值是否足够接近旧的估计值
        if abs(new_Xn - Xn) < tolerance:
            break

        # 更新估计值
        Xn = new_Xn

    return Xn
"""
        rendered_code = Code(
            code=code, tab_width=4, background="linux",
            language="Python", font="Monospace", style="emacs"
        )
        rendered_code.scale(0.9).set_opacity(0.8)

        self.play(Create(rendered_code))

        self.wait()

        end_log = self._end_logo()

        self.play(ReplacementTransform(VGroup(title, rendered_code), end_log[0]))

        self.play(ReplacementTransform(
            VGroup(graph, formual4, formual4_box, formual5),
            end_log[1]
        ))

        self.play(FadeOut(end_log), run_time=3)

    def _next_draw(self, graph, Xn):
        func = graph[0].plot(
            self._generate_linear_func(Xn),
            x_range=[1, 5],
            color=PURE_RED
        )
        func.set_stroke(width=1)
        Xn1 = self.nweton_sqrt_next(Xn)
        Xn1_line = graph[0].get_vertical_line(
            graph[0].input_to_graph_point(Xn1, graph[2]),
            color=YELLOW
        )

        self.play(Create(func))
        graph.add(func)
        self.play(Create(Xn1_line))
        graph.add(Xn1_line)

        Xn1_dot = Dot(graph[0].coords_to_point(Xn1, 0), color=PINK)
        self.play(Create(Xn1_dot))

        return Xn1, Xn1_dot

    def sqrt_newton(target, tolerance=0.0001):

        Xn = target # 牛顿迭代法的初始估计值

        while True:
            # 计算新的估计值 Xn+1 = Xn - F(Xn) / F'(Xn)
            new_Xn = Xn - (Xn * Xn - target) / (2 * Xn)

            # 检查新的估计值是否足够接近旧的估计值
            if abs(new_Xn - Xn) < tolerance:
                break

            # 更新估计值
            Xn = new_Xn

        return Xn

    def nweton_sqrt_next(self, x_n, target=2):
        # return Xn+1
        return x_n - (x_n * x_n - target) / (2 * x_n)

    def _generate_linear_func(self, x0):
        def f(x):
            return x0 * x0 - 2 + 2 * x0 * (x - x0)
        return f

if __name__ == "__main__":

    print(Newton.sqrt_newton(2))

    scene = Newton()

    scene.render()