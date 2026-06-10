from manim import *
from abc import ABC, abstractmethod

config.flush_cache = True

# ═══════════════════════════════════════════════════════════════════
#  1. Interfaces (Blueprints)
# ═══════════════════════════════════════════════════════════════════

class ITypography(ABC):
    """Interface for Course Typography & Color System."""
    @abstractmethod
    def bg(self) -> str: pass
    @abstractmethod
    def color_white(self) -> str: pass
    @abstractmethod
    def color_secondary(self) -> str: pass  # Subtitle এর জন্য সফট গ্রে
    @abstractmethod
    def color_red(self) -> str: pass
    @abstractmethod
    def color_yellow(self) -> str: pass
    @abstractmethod
    def color_blue(self) -> str: pass
    @abstractmethod
    def color_green(self) -> str: pass
    @abstractmethod
    def font_ui(self) -> str: pass
    @abstractmethod
    def font_code(self) -> str: pass
    @abstractmethod
    def title_size(self) -> int: pass
    @abstractmethod
    def dot_radius(self) -> float: pass


class IScreenTemplate(ABC):
    """Interface for Top-Left Tracker and Bottom-Left Lower Third."""
    # ── Top Left Tracker Methods ──
    @abstractmethod
    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None: pass
    @abstractmethod
    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None: pass
    @abstractmethod
    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None: pass
    @abstractmethod
    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None: pass
    @abstractmethod
    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None: pass

    # ── Lower Third Methods ──
    @abstractmethod
    def show_lower_third(self, title: str, subtitle: str, color_type: str = "blue") -> None: pass
    @abstractmethod
    def hide_lower_third(self) -> None: pass


# ═══════════════════════════════════════════════════════════════════
#  2. Concrete Implementations
# ═══════════════════════════════════════════════════════════════════

class Typography(ITypography):
    """Concrete implementation of the Typography design system."""
    def __init__(self):
        self.__BG         = "#121212"
        self.__WHITE      = "#E0E0E0"  # Primary Text (Off-white)
        self.__SECONDARY  = "#B0B0B0"  # Subtitle / Muted Text (Soft Gray)
        
        # Accent Colors
        self.__RED        = "#DC3545"  # Brute Force / Warning
        self.__YELLOW     = "#EAB308"  # Optimal / Important
        self.__BLUE       = "#1A73E8"  # Walkthrough / Info
        self.__GREEN      = "#198754"  # Success / Result

        self.__FONT_UI    = "Inter"
        self.__FONT_CODE  = "Fira Code"
        self.__SCENE_TITLE_SIZE = 28
        self.__DOT_RADIUS = 0.22

    def bg(self) -> str:             return self.__BG
    def color_white(self) -> str:    return self.__WHITE
    def color_secondary(self) -> str:return self.__SECONDARY
    def color_red(self) -> str:      return self.__RED
    def color_yellow(self) -> str:   return self.__YELLOW
    def color_blue(self) -> str:     return self.__BLUE
    def color_green(self) -> str:    return self.__GREEN

    def font_ui(self) -> str:        return self.__FONT_UI
    def font_code(self) -> str:      return self.__FONT_CODE
    def title_size(self) -> int:     return self.__SCENE_TITLE_SIZE
    def dot_radius(self) -> float:   return self.__DOT_RADIUS


class ScreenTemplate(IScreenTemplate):
    """Manages both Top-Left Tracker and Premium Lower Third overlays."""
    def __init__(self, scene: Scene, typo: ITypography = None):
        self.__scene = scene
        self.__typo = typo if typo else Typography()
        
        self.__scene.camera.background_color = self.__typo.bg()
        self.__current_tracker = None
        self.__current_lower_third = None

    # ── Private Helper: Top Tracker ──
    def __update_tracker(self, text: str, dot_color: str, run_time: float = 1.0):
        # Create new dot with dynamic color
        dot = Circle(
            radius=self.__typo.dot_radius(),
            color=dot_color,
            fill_opacity=1,
            stroke_width=0
        )
        
        # .upper() ব্যবহার করে যেকোনো ইনপুটকে ফোর্সড আপারকেস করা হলো 
        title_text = Text(
            text.upper(),  
            font=self.__typo.font_ui(),
            font_size=self.__typo.title_size(),
            color=self.__typo.color_white()
        )
        
        # Group and position at top-left
        new_tracker = VGroup(dot, title_text).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        new_tracker.to_edge(UP + LEFT, buff=0.5)

        # Smooth transition logic
        if self.__current_tracker is None:
            self.__scene.play(FadeIn(new_tracker, shift=RIGHT * 0.3), run_time=run_time)
        else:
            self.__scene.play(ReplacementTransform(self.__current_tracker, new_tracker), run_time=run_time)
        
        # Update state
        self.__current_tracker = new_tracker

    # ── Public Tracker Controls ──
    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None:
        self.__update_tracker(text, self.__typo.color_white())

    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None:
        self.__update_tracker(text, self.__typo.color_red())

    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None:
        self.__update_tracker(text, self.__typo.color_yellow())

    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None:
        self.__update_tracker(text, self.__typo.color_blue())

    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None:
        self.__update_tracker(text, self.__typo.color_green())

    # ── Public Lower Third Implementation ──
    def show_lower_third(self, title: str, subtitle: str, color_type: str = "blue") -> None:
        """
        Bottom-Left এ একটি প্রিমিয়াম লোয়ার-থার্ড পপআপ করবে।
        color_type হতে পারে: 'blue', 'red', 'yellow', 'green', 'white'
        """
        # ১. কালার ম্যাপ সিলেকশন
        color_map = {
            "white": self.__typo.color_white(),
            "red": self.__typo.color_red(),
            "yellow": self.__typo.color_yellow(),
            "blue": self.__typo.color_blue(),
            "green": self.__typo.color_green()
        }
        accent_color = color_map.get(color_type.lower(), self.__typo.color_blue())

        # ২. UI এলিমেন্ট তৈরি (ভার্টিকাল আক্সেন্ট লাইন + ২ লেয়ার টেক্সট)
        accent_bar = Line(UP * 0.45, DOWN * 0.45, stroke_width=5, color=accent_color)
        
        title_mob = Text(title, font=self.__typo.font_ui(), font_size=24, color=self.__typo.color_white(), weight=BOLD)
        subtitle_mob = Text(subtitle, font=self.__typo.font_code(), font_size=16, color=self.__typo.color_secondary())
        
        text_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        
        # এক সাথে গ্রুপ করে পজিশন সেট করা
        lt_group = VGroup(accent_bar, text_group).arrange(RIGHT, buff=0.25, aligned_edge=ORIGIN)
        lt_group.to_edge(DOWN + LEFT, buff=0.6)

        # ৩. অ্যানিমেশন এক্সিকিউশন (যদি অলরেডি স্ক্রিনে থাকে তবে ট্রান্সফর্ম হবে, না থাকলে স্মুথ রিভিল হবে)
        if self.__current_lower_third is not None:
            self.__scene.play(ReplacementTransform(self.__current_lower_third, lt_group), run_time=0.8)
        else:
            self.__scene.play(
                GrowFromCenter(accent_bar, run_time=0.4),
                FadeIn(text_group, shift=RIGHT * 0.3, run_time=0.6),
                rate_func=smooth
            )
        
        self.__current_lower_third = lt_group

    def hide_lower_third(self) -> None:
        """স্ক্রিন থেকে লোয়ার-থার্ডটি স্মুথলি রিমুভ করে দেবে"""
        if self.__current_lower_third is not None:
            self.__scene.play(FadeOut(self.__current_lower_third, shift=LEFT * 0.3), run_time=0.5)
            self.__current_lower_third = None


# ═══════════════════════════════════════════════════════════════════
#  3. Production Scene Demo
# ═══════════════════════════════════════════════════════════════════

class LowerThirdDemo(Scene):
    def construct(self):
        typo = Typography()
        ui = ScreenTemplate(self, typo)

        # ⚪ Phase 1: Analysis & Intro
        ui.screen_statement()
        ui.show_lower_third("Two Sum Problem", "LeetCode #1 — Difficulty: Easy", "white")
        self.wait(2)

        # 🔴 Phase 2: Brute Force (Line & Text Automatically Transforms!)
        ui.screen_brute_force()
        ui.show_lower_third("Brute Force Approach", "Time: O(N²) · Space: O(1)", "red")
        self.wait(2)

        # 🟡 Phase 3: Optimization Warning
        ui.screen_optimal_approach()
        ui.show_lower_third("Time Limit Exceeded?", "Nested loops fail on large datasets!", "yellow")
        self.wait(2)

        # 🔵 Phase 4: Walkthrough
        ui.screen_code_walkthrough()
        ui.show_lower_third("Optimal Solution", "Using HashMap · Time: O(N) · Space: O(N)", "blue")
        self.wait(2)

        # 🟢 Phase 5: Clear for Final Submission
        ui.screen_code_submission()
        ui.hide_lower_third()  # কোড সাবমিশনের সময় ডোপামিন হিট বাড়াতে লোয়ার থার্ড হাইড করা হলো
        self.wait(2)
