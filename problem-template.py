```python
from manim import *

# ═══════════════════════════════════════════════════════════════════
#  CourseTheme
#  Single source of truth for ALL colors, typography, and semantic
#  roles — sourced directly from color-phycology-v2.md spec.
# ═══════════════════════════════════════════════════════════════════
class CourseTheme:

    # ── raw palette (name-mangled = inaccessible outside class) ──
    __BG         = "#121212"
    __BLUE       = "#1A73E8"
    __GREEN      = "#198754"
    __RED        = "#DC3545"
    __YELLOW     = "#EAB308"
    __ORANGE     = "#F97316"
    __WHITE      = "#E0E0E0"
    __GRAY       = "#424242"
    __PURE_WHITE = "#FFFFFF"   # text on dark/blue/red/green fills
    __PURE_BLACK = "#000000"   # text on yellow/bright fills

    # ── typography & sizes ───────────────────────────────────────
    __FONT_UI   = "Inter"
    __FONT_CODE = "Fira Code"
    __FS_TITLE  = 52
    __FS_BODY   = 32
    __FS_LABEL  = 24
    __FS_SMALL  = 20
    __STROKE    = 2.5   # 2px–3px per spec for crisp 480p+ video

    # ── Scene Title & Dot variables (NEW) ────────────────────────
    __DOT_RADIUS        = 0.18       # অপটিমাইজড সাইজ (টেক্সটের সাথে ব্যালেন্সড)
    __DOT_COLOR         = __WHITE    
    __SCENE_TITLE_SIZE  = 32         
    __SCENE_TITLE_COLOR = __WHITE    

    # ── background ───────────────────────────────────────────────
    def bg(self)              -> str:   return self.__BG

    # ── node/element colors ──────────────────────────────────────
    def node_blue(self)       -> str:   return self.__BLUE
    def node_green(self)      -> str:   return self.__GREEN
    def node_red(self)        -> str:   return self.__RED
    def node_yellow(self)     -> str:   return self.__YELLOW
    def node_orange(self)     -> str:   return self.__ORANGE
    def node_white(self)      -> str:   return self.__WHITE
    def node_gray(self)       -> str:   return self.__GRAY

    # ── text colors (per spec rules) ─────────────────────────────
    def text_on_dark(self)    -> str:   return self.__PURE_WHITE
    def text_on_yellow(self)  -> str:   return self.__PURE_BLACK
    def text_white(self)      -> str:   return self.__WHITE
    def text_gray(self)       -> str:   return self.__GRAY

    # ── typography & sizes ───────────────────────────────────────
    def font(self)             -> str:  return self.__FONT_UI
    def font_code(self)        -> str:  return self.__FONT_CODE
    def font_size_title(self)  -> int:  return self.__FS_TITLE
    def font_size_body(self)   -> int:  return self.__FS_BODY
    def font_size_label(self)  -> int:  return self.__FS_LABEL
    def font_size_small(self)  -> int:  return self.__FS_SMALL
    def stroke_width(self)     -> float: return self.__STROKE

    # ── Scene Title & Dot Getters (NEW) ──────────────────────────
    def dot_radius(self)        -> float: return self.__DOT_RADIUS
    def dot_color(self)         -> str:   return self.__DOT_COLOR
    def scene_title_size(self)  -> int:   return self.__SCENE_TITLE_SIZE
    def scene_title_color(self) -> str:   return self.__SCENE_TITLE_COLOR


# ═══════════════════════════════════════════════════════════════════
#  CourseAnimator
#  Takes a Scene + CourseTheme. All color/font choices come from
#  the theme — nothing is hardcoded here.
# ═══════════════════════════════════════════════════════════════════
class CourseAnimator:

    def __init__(self, scene: Scene, theme: CourseTheme = None):
        self.__scene = scene
        self.__t     = theme if theme else CourseTheme()
        self.__scene.camera.background_color = self.__t.bg()

    # ── public interface ─────────────────────────────────────────

    def play_intro(self, title: str, subtitle: str = ""):
        t1, t2 = self.__build_intro(title, subtitle)
        self.__anim_intro(t1, t2)

    def play_section_title(self, section: str, number: int = 0):
        n, s, l = self.__build_section_title(section, number)
        self.__anim_section_title(n, s, l)

    def play_callout(self, text: str, position=None):
        if position is None:
            position = DOWN * 1.5
        box, label = self.__build_callout(text, position)
        self.__anim_callout(box, label)

    def play_lower_third(self, name: str, role: str = ""):
        bar, nm, rm = self.__build_lower_third(name, role)
        self.__anim_lower_third(bar, nm, rm)

    def play_outro(self, message: str = "See you in the next lesson!"):
        mob = self.__build_outro(message)
        self.__anim_outro(mob)

    def clear_screen(self, run_time: float = 0.6):
        if self.__scene.mobjects:
            self.__scene.play(
                *[FadeOut(m) for m in self.__scene.mobjects],
                run_time=run_time
            )

    # ── private builders ─────────────────────────────────────────

    def __build_intro(self, title, subtitle):
        t = self.__t
        title_mob = Text(title, font=t.font(),
                         font_size=t.font_size_title(),
                         color=t.node_blue(), weight=BOLD
                         ).move_to(UP * 0.4)
        sub_mob = (
            Text(subtitle, font=t.font(),
                 font_size=t.font_size_small(),
                 color=t.text_white())
            .next_to(title_mob, DOWN, buff=0.35)
        ) if subtitle else VMobject()
        return title_mob, sub_mob

    def __build_section_title(self, section, number):
        t = self.__t
        num_mob = Text(f"{number:02d}" if number else "",
                       font=t.font(), font_size=80,
                       color=t.node_yellow(), weight=BOLD
                       ).move_to(LEFT * 3)
        sec_mob = Text(section, font=t.font(),
                       font_size=t.font_size_body(),
                       color=t.text_white()
                       ).move_to(RIGHT * 1.2)
        line = Line(LEFT * 0.2 + UP * 1.5, LEFT * 0.2 + DOWN * 1.5,
                    color=t.node_blue(), stroke_width=t.stroke_width())
        return num_mob, sec_mob, line

    def __build_callout(self, text, position):
        t = self.__t
        label = Text(text, font=t.font(),
                     font_size=t.font_size_label(),
                     color=t.text_on_dark()
                     ).move_to(position)
        box = SurroundingRectangle(
            label, color=t.node_yellow(),   # YELLOW = active attention
            buff=0.25, corner_radius=0.12,
            stroke_width=t.stroke_width()
        )
        return box, label

    def __build_lower_third(self, name, role):
        t = self.__t
        bar = Rectangle(width=config.frame_width, height=0.9,
                        fill_color=t.node_blue(), fill_opacity=0.92,
                        stroke_width=0).to_edge(DOWN, buff=0)
        nm  = Text(name, font=t.font(), font_size=30,
                   color=t.text_on_dark(), weight=BOLD
                   ).move_to(bar.get_center() + LEFT * 3 + UP * 0.05)
        rm  = (
            Text(role, font=t.font(),
                 font_size=t.font_size_small(),
                 color=t.text_on_dark())
            .next_to(nm, RIGHT, buff=0.5)
        ) if role else VMobject()
        return bar, nm, rm

    def __build_outro(self, message):
        t = self.__t
        return Text(message, font=t.font(),
                    font_size=t.font_size_body(),
                    color=t.node_green()     # GREEN = success / lesson complete
                    ).move_to(ORIGIN)

    # ── private animators ────────────────────────────────────────

    def __anim_intro(self, title_mob, sub_mob):
        self.__scene.play(Write(title_mob, run_time=1.2))
        if isinstance(sub_mob, Text):
            self.__scene.play(FadeIn(sub_mob, shift=UP * 0.2, run_time=0.8))
        self.__scene.wait(1.5)

    def __anim_section_title(self, num_mob, sec_mob, line):
        self.__scene.play(
            FadeIn(num_mob, shift=RIGHT * 0.4, run_time=0.6),
            GrowFromCenter(line, run_time=0.5),
        )
        self.__scene.play(Write(sec_mob, run_time=0.8))
        self.__scene.wait(1.2)

    def __anim_callout(self, box, label):
        self.__scene.play(Create(box, run_time=0.5), Write(label, run_time=0.6))
        self.__scene.wait(1.8)

    def __anim_lower_third(self, bar, nm, rm):
        bar.shift(DOWN * bar.height)
        self.__scene.add(bar)
        self.__scene.play(bar.animate.shift(UP * bar.height), run_time=0.5)
        self.__scene.play(
            Write(nm, run_time=0.6),
            FadeIn(rm, run_time=0.5) if isinstance(rm, Text) else Wait(0),
        )
        self.__scene.wait(2)
        self.__scene.play(FadeOut(bar), FadeOut(nm), FadeOut(rm), run_time=0.4)

    def __anim_outro(self, mob):
        self.__scene.play(FadeIn(mob, run_time=0.8))
        self.__scene.wait(1.5)
        self.__scene.play(FadeOut(mob, run_time=1.2))


# ═══════════════════════════════════════════════════════════════════
#  DemoScene  —  usage template
#  Run:  manim -pql course_animator.py DemoScene
# ═══════════════════════════════════════════════════════════════════
class DemoScene(Scene):

    def construct(self):
        theme = CourseTheme()            # ← single source of all colors/fonts
        anim  = CourseAnimator(self, theme)

        # ── intro ─────────────────────────────────────────────────
        anim.play_intro(
            title="Data Structures & Algorithms",
            subtitle="Udemy · Complete Course"
        )
        anim.clear_screen()

        # ── section card ──────────────────────────────────────────
        anim.play_section_title(section="Arrays & Hashing", number=1)
        anim.clear_screen()

        # ── node state demo (use theme directly in your Scenes) ───
        # YELLOW = current active pointer
        active = Circle(radius=0.5, color=theme.node_yellow(),
                        fill_opacity=1).move_to(LEFT * 3)
        active_lbl = Text("i", font=theme.font_code(), font_size=28,
                          color=theme.text_on_yellow()
                          ).move_to(active.get_center())

        # BLUE = in-queue / processing
        inq = Circle(radius=0.5, color=theme.node_blue(),
                     fill_opacity=1).move_to(LEFT * 1)
        inq_lbl = Text("j", font=theme.font_code(), font_size=28,
                       color=theme.text_on_dark()
                       ).move_to(inq.get_center())

        # ORANGE = already visited (NOT green per spec)
        visited = Circle(radius=0.5, color=theme.node_orange(),
                         fill_opacity=1).move_to(RIGHT * 1)
        visited_lbl = Text("k", font=theme.font_code(), font_size=28,
                           color=theme.text_on_dark()
                           ).move_to(visited.get_center())

        # WHITE/GRAY = unvisited static node
        unvisited = Circle(radius=0.5, color=theme.node_gray(),
                           fill_opacity=1).move_to(RIGHT * 3)
        unvisited_lbl = Text("l", font=theme.font_code(), font_size=28,
                             color=theme.text_on_dark()
                             ).move_to(unvisited.get_center())

        self.play(
            FadeIn(active), FadeIn(active_lbl),
            FadeIn(inq), FadeIn(inq_lbl),
            FadeIn(visited), FadeIn(visited_lbl),
            FadeIn(unvisited), FadeIn(unvisited_lbl),
        )
        self.wait(1)

        # inq node → SUCCESS (GREEN = target found!)
        self.play(
            inq.animate.set_fill(theme.node_green()).set_stroke(theme.node_green()),
        )
        self.wait(1)
        anim.clear_screen()

        # ── callout over code ─────────────────────────────────────
        code = Text("arr = [3, 1, 4, 1, 5, 9]",
                    font=theme.font_code(),
                    font_size=theme.font_size_body(),
                    color=theme.text_white()
                    ).move_to(UP * 1)
        self.play(Write(code))
        self.wait(0.3)
        anim.play_callout("O(n) time!", position=DOWN * 1.5)
        anim.clear_screen()

        # ── lower third + outro ───────────────────────────────────
        anim.play_lower_third(name="Barik", role="DSA Instructor")
        anim.play_outro("See you in the next lesson!")

```
