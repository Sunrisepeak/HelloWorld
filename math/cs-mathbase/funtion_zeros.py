from manim import *
from logo import CSMathBase

"""

Wiki: https://zh.wikipedia.org/zh-cn/%E7%89%9B%E9%A1%BF%E6%B3%95

python3 math/cs-mathbase/funtion_zeros.py

manim -pql math/cs-mathbase/funtion_zeros.py BinarySearch

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

class BinarySearch(CSMathBase):
    def construct(self):
        start_logo, start_logo_title = self._start_logo()

        title = VGroup(
            Text("sqrt()平方根计算实现").set_color(YELLOW),
            Text("之一 - 二分法", t2c={"之一": PURE_RED, "二分法": BLUE})
        ).arrange(RIGHT)

        self.play(ReplacementTransform(start_logo, title[0]))

        self.play(ReplacementTransform(start_logo_title, title[1]))

        self.wait()

        segments = VGroup(
            Text("1. 二分法简介"),
            Text("2. 问题的数学表示"),
            Text("3. 求解过程演示&代码实现"),
        ).arrange(DOWN, aligned_edge=LEFT).set_opacity(0.5)

        self.play(
            title.animate.to_corner(UP),
            FadeIn(segments)
        )

        self.wait()

        segments[0].set_opacity(1)

        self.wait()

        binary_search_overview = ImageMobject("imgs/math/function_zeros.1.png")
        binary_search_overview.scale(1.1)

        self.play(FadeIn(binary_search_overview))

        self.wait()

        self.play(binary_search_overview.animate.scale(0))

        self.wait()
        
        segments[0].set_opacity(0.3)
        segments[1].set_opacity(1)

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
        ).scale(0.8)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x) = x^2 - 2")
        func_graph = axes.plot(lambda x: x * x - 2, x_range=[-2, 5], color=BLUE).set_stroke(width=1)

        graph = VGroup(axes, axes_labels.scale(0.7), func_graph)

        formulas = VGroup(
            MathTex(r"\sqrt{a} = X"),
            MathTex(r"a = X^2"),
            MathTex(r"f(x) = x^2 - a")
        ).arrange(DOWN).scale(0.8).to_corner(LEFT)

        self.play(
            FadeOut(segments),
            Create(graph),
            Create(formulas)
        )

        self.wait()

        formula_box = SurroundingRectangle(formulas[0])

        self.play(Create(formula_box))

        self.wait()

        old_formula_box = formula_box
        formula_box = SurroundingRectangle(formulas[1])

        self.play(ReplacementTransform(old_formula_box, formula_box))

        self.wait()

        old_formula_box = formula_box
        formula_box = SurroundingRectangle(formulas[2])

        self.play(ReplacementTransform(old_formula_box, formula_box))

        self.wait()

        self.play(
            FadeIn(segments),
            FadeOut(VGroup(formula_box, formulas, graph))
        )

        segments[1].set_opacity(0.3)
        segments[2].set_opacity(1)

        self.wait()

        self.play(
            FadeOut(segments),
            FadeIn(graph)
        )

        self.wait()

        sqrt_2 = VGroup(
            Text("求解"),
            MathTex(r"\sqrt{2}"),
            Text("误差 0.01")
        ).arrange(RIGHT).scale(0.7)

        self.play(Write(sqrt_2))

        self.wait()

        lines = VGroup()
        
        # Generate lines for the specified x_range from 0 to 2 with a step of 0.01
        for x in np.arange(0, 2, 0.01):
            line = Line(
                start=axes.c2p(x, 0),
                end=axes.c2p(x, (lambda x: x**2 - 2)(x)),
                stroke_width=0.3,
                color=BLUE if int((x * 100) % 2) == 0 else YELLOW
            )
            lines.add(line)

        self.camera.frame.save_state()

        scale_center_point = graph[0].coords_to_point(1, 0)

        self.play(self.camera.frame.animate.scale(0.25).move_to(scale_center_point))

        pixel_delta = scale_center_point[0]

        title_2 = Text(
            "以0.01为间隔做离散化",
            t2c={"离散化": PURE_RED}
        ).move_to([pixel_delta, pixel_delta - 0.4, 0])
        title_2.scale(0.2)

        self.play(
            Create(lines),
            Write(title_2)
        )

        self.wait()

        array_info = Text(
            "f(index/tolerance)_value[0,..,200]",
            t2c={"f(index/tolerance)_value": BLUE}
        ).move_to([pixel_delta, pixel_delta - 0.6, 0])
        array_info.scale(0.15)

        self.play(Write(array_info))

        self.wait()

        def f(x):
            return x * x - 2

        interval = [0, 2]
        tolerance = 0.01
        def compute():
            mid = (interval[0] + interval[1]) / 2

            fx_value = f(mid)

            if fx_value > 0:
                interval[1] = mid
            else:
                interval[0] = mid

            mid_dot = Dot(graph[0].coords_to_point(mid, 0)).set_color(PINK).scale(0.2)

            self.play(Create(mid_dot))

            graph.add(mid_dot)

            for value in np.arange(0, interval[0], 0.01):
                lines[int(value * 100)].set_opacity(0.3)

            self.wait(0.5)

            for value in np.arange(interval[1], 2, 0.01):
                lines[int(value * 100)].set_opacity(0.3)

            compute_completed = False

            if abs(interval[1] - interval[0]) < tolerance:
                compute_completed = True

            return compute_completed, mid, fx_value

        ok, x, fx = (False, 2, 2)

        x_and_fx = Text(
            'f({:.3f}) = X * X - 2 = {:.2f}'.format(x, fx),
        ).move_to([pixel_delta, pixel_delta - 1.5, 0]).scale(0.15)

        interval_len = Text(
            '< {:.3f} >'.format(interval[1] - interval[0]),
            t2c={'{:.3f}'.format(interval[1] - interval[0]) : YELLOW}
        ).move_to([pixel_delta, pixel_delta - 0.2, 0]).scale(0.2)

        search_interval = Text(
            '查找区间[{:.3f}, {:.3f}]'.format(interval[0], interval[1])
        )
        search_interval.move_to([pixel_delta, pixel_delta - 0.8, 0]).scale(0.15)

        self.play(Create(VGroup(search_interval, x_and_fx, interval_len)))

        while ok == False:
            old_x_and_fx = x_and_fx
            old_search_interval = search_interval
            old_interval_len = interval_len

            ok, x, fx = compute()

            print('f({:.2f}) = {:.6f}'.format(x, fx))

            x_and_fx = Text(
                'f({:.5f}) = X * X - 2 = {:.4f}'.format(x, fx),
                t2c={
                    '{:.5f}'.format(x) : BLUE,
                    '{:.4f}'.format(fx): PURE_GREEN
                }
            ).move_to([pixel_delta, pixel_delta - 1.5, 0]).scale(0.15)

            interval_len = Text(
                '< {:.3f} >'.format(interval[1] - interval[0]),
                t2c={'{:.3f}'.format(interval[1] - interval[0]) : YELLOW}
            ).move_to([pixel_delta, pixel_delta - 0.2, 0]).scale(0.2)

            search_interval = Text(
                '查找区间[{:.3f}, {:.3f}]'.format(interval[0], interval[1]),
            )
            search_interval.move_to([pixel_delta, pixel_delta - 0.8, 0]).scale(0.15)

            self.play(ReplacementTransform(
                VGroup(old_x_and_fx, old_search_interval, old_interval_len),
                VGroup(x_and_fx, search_interval, interval_len)
            ))

        self.wait()

        self.play(Restore(self.camera.frame))

        self.wait()

        code = """
# 计算平方根: f(x) = x^2 - a
def sqrt_binary_serach(target, tolerance=0.001):
    #assert target > 0
    interval = [0, target]

    def f(x):
        return x * x - target

    fx_value = f(target)

    while True:
        # 计算新的估计值 Xn+1 = Xn - F(Xn) / F'(Xn)
        mid = (interval[0] + interval[1]) / 2
        fx_value = f(mid)
        if fx_value == 0:
            return mid
        if fx_value > 0:
            interval[1] = mid # 更新区间右值
        else:
            interval[0] = mid # 更新区间左值
        # 计算误差, 符合要求误差就break出
        if abs(interval[0] - interval[1]) < tolerance:
            break

    return interval[0]
"""
        rendered_code = Code(
            code=code, tab_width=4, background="linux",
            language="Python", font="Monospace", style="emacs"
        )
        rendered_code.scale(0.8).set_opacity(0.8)

        self.play(Create(rendered_code))

        self.wait()

        #print(str(self.sqrt_binary_serach(2)))

        end_log = self._end_logo()

        self.play(ReplacementTransform(VGroup(title, title_2, sqrt_2, rendered_code), end_log[0]))

        self.play(ReplacementTransform(
            VGroup(graph, array_info, interval_len, search_interval, x_and_fx),
            end_log[1]
        ))

        self.play(FadeOut(end_log), run_time=3)

    def sqrt_binary_serach(self, target, tolerance=0.001):
        #assert target > 0
        interval = [0, target]

        def f(x):
            return x * x - target

        fx_value = f(target)

        while True:
            # 计算新的估计值 Xn+1 = Xn - F(Xn) / F'(Xn)
            mid = (interval[0] + interval[1]) / 2
            fx_value = f(mid)
            if fx_value == 0:
                return mid
            if fx_value > 0:
                interval[1] = mid # 更新区间右值
            else:
                interval[0] = mid # 更新区间左值
            # 计算误差, 符合要求误差就break出
            if abs(interval[0] - interval[1]) < tolerance:
                break

        return interval[0]

if __name__ == "__main__":

    #print(Newton.sqrt_newton(2))

    #scene = Newton()
    scene = BinarySearch()

    #print(str(scene.sqrt_binary_serach(2)))

    scene.render()