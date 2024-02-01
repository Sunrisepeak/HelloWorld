from manim import *

"""
manim -pql thinking/fans_or_follower.py FansOrFollower

"""

class FansOrFollower(Scene):
    def construct(self):
        question = self._question()
        p_info = self._platform_info()

        platform_title = Text("社区平台").set_color(YELLOW)
        platform_title.to_corner(UL)

        self.play(
            ReplacementTransform(question, platform_title),
            FadeIn(p_info)
        )

        self.wait()

        platform1 = VGroup(
            Text("面向生活&娱乐的平台").set_color(PINK),
            Text("往往更喜欢用粉丝这个词, 有助于拉近彼此距离强调感性", t2c={"粉丝": PINK, "拉近彼此距离强调感性": PINK})
        ).arrange(DOWN, buff=0.2, center=True).scale(0.8)

        platform2 = VGroup(
            Text("讨论&技术的平台").set_color(BLUE),
            Text("更喜欢使用关注者这个词, 强调关系中的理性", t2c={"关注者": BLUE, "强调关系中的理性": BLUE})
        ).arrange(DOWN, buff=0.2, center=True).scale(0.8)

        platforms = VGroup(platform2, platform1).arrange(DOWN, buff=1)

        platform1_box = SurroundingRectangle(platforms[0]).set_color(PURE_RED)
        platform2_box = SurroundingRectangle(platforms[1]).set_color(ORANGE)

        self.play(
            ApplyMethod(p_info.set_opacity, 0.2),
            Create(platforms),
        )

        self.wait()

        self.play(Create(platform1_box))

        self.wait()

        self.play(ReplacementTransform(platform1_box, platform2_box))

        self.play(FadeOut(VGroup(platform_title, platforms, platform1_box, platform2_box)))

        p_info.set_opacity(0)

        self._llm_response()

    def _question(self):

        fans = Text("粉丝", color=PINK).scale(1.5).rotate(15 * DEGREES)
        follower = Text("关注者", color=BLUE).scale(1.5).rotate(-15 * DEGREES)

        ff = VGroup(fans, follower).arrange(RIGHT, buff=1)

        ff.move_to(2 * UP)

        self.play(
            Write(ff[1]),
            Write(ff[0])
        )

        self.wait()

        question1 = Text("你们觉得这两个词有差别吗?").scale(1.3)
        self.play(FadeIn(question1))

        self.wait()

        texts = VGroup(
            Text("有些人表示不关心", t2c={"不关心": GREEN}),
            Text("有些人感觉用粉丝这个词更温暖", t2c={"温暖": PINK}),
            Text("有些人感觉用关注者这个词更理性", t2c={"理性": BLUE}),
        ).arrange(DOWN, buff=0.2, center=True).scale(0.7)

        texts.move_to(2 * DOWN)

        self.play(Create(texts))

        self.wait()

        # 如果你认为有区别
        question2 = VGroup(
            Text("你认为你是关注者还是粉丝呢?", t2c={"粉丝": PINK, "关注者": BLUE}),
            Text("你认为关注你的对象是粉丝还是关注者呢?", t2c={"粉丝": PINK, "关注者": BLUE})
        ).arrange(DOWN, buff=0.5)

        self.play(
            ReplacementTransform(VGroup(ff, question1), question2[0])
        )

        self.play(ReplacementTransform(texts, question2[1]))

        return question2

    def _platform_info(self):
        p_info = ImageMobject("imgs/thinking/fans-or-follower.0.png")
        p_info.set_opacity(0.8)
        return p_info

    def _llm_response(self):
        gpt_title = Text("GPT", color=YELLOW)
        gpt_title.to_corner(LEFT + UP)

        gpt_3_image = ImageMobject("imgs/thinking/fans-or-follower.1.png")
        gpt_3_image.scale(2).move_to(7 * DOWN).set_opacity(0.8)

        self.play(
            FadeIn(gpt_title),
            FadeIn(gpt_3_image)
        )

        self.play(
            gpt_3_image.animate.shift(12 * UP),
            self._progress_bar_animate(),
            run_time=5,
            rate_func=linear
        )

        self.wait() #5

        gpt_wxyy_image = ImageMobject("imgs/thinking/fans-or-follower.2.png")
        gpt_wxyy_image.scale(1.3).move_to(8 * DOWN).set_opacity(0.8)

        self.play(
            gpt_3_image.animate.shift(10 * UP),
            gpt_wxyy_image.animate.shift(8 * UP),
            self._progress_bar_animate(RED, PURE_RED),
            run_time=5,
            rate_func=linear
        )

        self.wait() #5

        gpt_4_image = ImageMobject("imgs/thinking/fans-or-follower.3.png")
        gpt_4_image.scale(1.9).move_to(12 * DOWN).set_opacity(0.8)

        self.play(
            gpt_wxyy_image.animate.shift(15 * UP),
            gpt_4_image.animate.shift(17 * UP),
            self._progress_bar_animate(BLUE, PURE_BLUE),
            run_time=5,
            rate_func=linear
        )

        self.wait()

    def _progress_bar_animate(self, line_col=GREEN, dot_col=PURE_GREEN):
        d1 = Dot(4 * DR + RIGHT * 2).set_color(dot_col)
        l1 = Line(4 * DR + RIGHT * 2, 4 * UR + RIGHT * 2).set_stroke(width=5)
        l2 = VMobject()
        self.add(d1, l1, l2)
        l2.add_updater(lambda x:
            x.become(Line(4 * DR + RIGHT * 2, d1.get_center()).set_color(line_col)).set_stroke(width=5))
        return MoveAlongPath(d1, l1)

if __name__ == "__main__":
    scene = FansOrFollower()
    scene.render()