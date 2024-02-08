from manim import *
from logo import CSMathBase

class BinarySearch(CSMathBase):
    def construct(self):
        start_logo, start_logo_title = self._start_logo()

        title =  Text("根号2近似计算 - 二分法").scale(1.3)
        title.set_color(YELLOW)
        title.to_corner(UP)

        self.play(ReplacementTransform(VGroup(start_logo_title, start_logo), title))

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
            x_range=[-1, 3],
            y_range=[-4, 4],
            axis_config={"color": GREEN},
            tips=False,
        ).scale(0.6).to_corner(LEFT)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x) = x^2 - 2")
        func_graph = axes.plot(lambda x: x * x - 2, x_range=[-1, 2.3], color=BLUE)

        graph = VGroup(axes, axes_labels, func_graph)

        formual4 = MathTex("f(x1)f(x2) < 0").move_to(3 * DOWN)

        self.play(
            ReplacementTransform(formual3, formual4),
            Create(graph)
        )

        self.wait()



if __name__ == "__main__":
    scene = BinarySearch()
    scene.render()