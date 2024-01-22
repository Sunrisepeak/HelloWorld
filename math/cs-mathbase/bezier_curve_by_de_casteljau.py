from manim import *

"""

python3 math/cs-mathbase/bezier_curve_by_de_casteljau.py

"""

class BezierCurve(Scene):
    def construct(self):

        dots = self._point_to_curve()

        #self._de_casteljau()
        transform_title = Text("贝塞尔曲线(Bézier Curve) - De Casteljau算法动画").scale(0.70).to_edge(UP)
        transform_title.to_corner(UP + LEFT)

        self.play(Transform(dots, transform_title))
        self.wait()

    def _point_to_curve(self):

        tile = Text("贝塞尔曲线(Bézier Curve) 动画").scale(0.75).to_edge(UP)
        self.play(Write(tile))
        self.wait()

        d1 = Dot(point=DOWN + LEFT * 2).set_color(RED)
        d2 = Dot(point=UP + LEFT).set_color(GREEN)
        d3 = Dot(point=UP + RIGHT).set_color(BLUE)
        d4 = Dot(point=DOWN + RIGHT * 2).set_color(YELLOW)

        self.play(Create(VGroup(d1, d2, d3, d4)))

        def draw_curve():
            bezier = CubicBezier(d1.get_center(), d2.get_center(), d3.get_center(), d4.get_center())
            bezier.set_color(PINK)
            return bezier

        bezier = always_redraw(draw_curve)

        self.play(Create(bezier))
        self.play(d1.animate.shift(DL))
        self.play(d3.animate.shift(UP))

        l1 = always_redraw(lambda: Line(d1.get_center(), d2.get_center()).set_stroke(width=3, color=GRAY))
        l2 = always_redraw(lambda: Line(d3.get_center(), d4.get_center()).set_stroke(width=3, color=GRAY)) 

        self.play(Create(VGroup(l1, l2)))
        self.play(d2.animate.shift(LEFT * 2))
        self.play(d2.animate.shift(RIGHT))

        self.play(Uncreate(VGroup(tile, l1, l2, bezier)))

        return VGroup(d1, d2, d3, d4)

if __name__ == "__main__":
    scene = BezierCurve()
    scene.render()