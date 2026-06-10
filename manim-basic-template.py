from manim import *
from abc import ABC, abstractmethod

config.flush_cache = True

# ═══════════════════════════════════════════════════════════════════
#  0. Bulletproof Custom Rate Function
# ═══════════════════════════════════════════════════════════════════
def custom_ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


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
    def color_secondary(self) -> str: pass
    @abstractmethod
    def color_red(self) -> str: pass
    @abstractmethod
    def color_yellow(self) -> str: pass
    @abstractmethod
    def color_blue(self) -> str: pass
    @abstractmethod
    def color_green(self) -> str: pass
    @abstractmethod
    def color_milestone_green(self) -> str: pass
    @abstractmethod
    def font_ui(self) -> str: pass
    @abstractmethod
    def font_code(self) -> str: pass
    @abstractmethod
    def title_size(self) -> int: pass
    @abstractmethod
    def dot_radius(self) -> float: pass


class IScreenTemplate(ABC):
    """Interface for Top Left Status Trackers."""
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


class ILowerThird(ABC):
    """Interface for Dynamic Lower Third Components."""
    @abstractmethod
    def utils_lower_third_show(self, title: str, subtitle: str, color_type: str = "blue") -> None: pass
    @abstractmethod
    def utils_lower_third_hide(self) -> None: pass


class IIntroOutro(ABC):
    """Interface for Premium Lesson Transitions and Final Flows."""
    @abstractmethod
    def intro_lecture(self, title: str) -> None: pass
    @abstractmethod
    def intro_section(self, title: str) -> None: pass
    @abstractmethod
    def outro_lecture(self, next_topic: str) -> None: pass
    @abstractmethod
    def outro_section(self, section_title: str, challenges: list, next_module: str) -> None: pass


# ═══════════════════════════════════════════════════════════════════
#  2. Concrete Implementations
# ═══════════════════════════════════════════════════════════════════

class Typography(ITypography):
    def __init__(self):
        self.__BG               = "#121212"
        self.__WHITE            = "#E0E0E0"  
        self.__SECONDARY        = "#B0B0B0"  
        self.__RED              = "#DC3545"  
        self.__YELLOW           = "#EAB308"  
        self.__BLUE             = "#1A73E8"  
        self.__GREEN            = "#198754"  
        self.__MILESTONE_GREEN  = "#4CAF50"  

        self.__FONT_UI    = "Inter"
        self.__FONT_CODE  = "Fira Code"
        self.__SCENE_TITLE_SIZE = 32
        self.__DOT_RADIUS = 0.22

    def bg(self) -> str:                    return self.__BG
    def color_white(self) -> str:           return self.__WHITE
    def color_secondary(self) -> str:       return self.__SECONDARY
    def color_red(self) -> str:             return self.__RED
    def color_yellow(self) -> str:          return self.__YELLOW
    def color_blue(self) -> str:            return self.__BLUE
    def color_green(self) -> str:           return self.__GREEN
    def color_milestone_green(self) -> str: return self.__MILESTONE_GREEN
    def font_ui(self) -> str:               return self.__FONT_UI
    def font_code(self) -> str:             return self.__FONT_CODE
    def title_size(self) -> int:            return self.__SCENE_TITLE_SIZE
    def dot_radius(self) -> float:          return self.__DOT_RADIUS


class ScreenTemplate(IScreenTemplate):
    def __init__(self, scene: Scene, typo: ITypography):
        self.__scene = scene
        self.__typo = typo
        self.__current_tracker = None

    def __update_tracker(self, text: str, dot_color: str, run_time: float = 1.0):
        dot = Circle(radius=self.__typo.dot_radius(), color=dot_color, fill_opacity=1, stroke_width=0)
        # রিকোয়ারমেন্ট অনুযায়ী এখানে কোনো এক্সট্রা কার্নিং বা স্পেস এড করা হয়নি, নরমাল স্পেস জেনারেট হবে
        processed_text = text.upper() 
        title_text = Text(processed_text, font=self.__typo.font_ui(), font_size=self.__typo.title_size(), color=self.__typo.color_white())
        new_tracker = VGroup(dot, title_text).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        new_tracker.to_edge(UP + LEFT, buff=0.5)

        if self.__current_tracker is None:
            self.__scene.play(FadeIn(new_tracker, shift=RIGHT * 0.3), run_time=run_time)
        else:
            self.__scene.play(ReplacementTransform(self.__current_tracker, new_tracker), run_time=run_time)
        self.__current_tracker = new_tracker

    def screen_statement(self, text: str = "PROBLEM ANALYSIS") -> None: self.__update_tracker(text, self.__typo.color_white())
    def screen_brute_force(self, text: str = "BRUTE FORCE") -> None: self.__update_tracker(text, self.__typo.color_red())
    def screen_optimal_approach(self, text: str = "OPTIMAL APPROACH") -> None: self.__update_tracker(text, self.__typo.color_yellow())
    def screen_code_walkthrough(self, text: str = "CODE WALKTHROUGH") -> None: self.__update_tracker(text, self.__typo.color_blue())
    def screen_code_submission(self, text: str = "CODE SUBMISSION") -> None: self.__update_tracker(text, self.__typo.color_green())


class LowerThird(ILowerThird):
    def __init__(self, scene: Scene, typo: ITypography):
        self.__scene = scene
        self.__typo = typo
        self.__current_lower_third = None

    def utils_lower_third_show(self, title: str, subtitle: str, color_type: str = "blue") -> None:
        color_map = {
            "white": self.__typo.color_white(), 
            "red": self.__typo.color_red(), 
            "yellow": self.__typo.color_yellow(), 
            "blue": self.__typo.color_blue(), 
            "green": self.__typo.color_green()
        }
        accent_color = color_map.get(color_type.lower(), self.__typo.color_blue())

        if self.__current_lower_third is not None:
            self.utils_lower_third_hide()

        accent_bar = Line(UP * 0.45, DOWN * 0.45, stroke_width=5, color=accent_color)
        title_mob = Text(title, font=self.__typo.font_ui(), font_size=24, color=self.__typo.color_white(), weight=BOLD)
        subtitle_mob = Text(subtitle, font=self.__typo.font_code(), font_size=16, color=self.__typo.color_secondary())
        text_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        new_lt = VGroup(accent_bar, text_group).arrange(RIGHT, buff=0.25, aligned_edge=ORIGIN)
        new_lt.to_edge(DOWN + LEFT, buff=0.6)

        lt_height = new_lt.height
        reveal_mask = Rectangle(width=new_lt.width + 1.0, height=lt_height + 1.0, fill_color=self.__typo.bg(), fill_opacity=1, stroke_width=0).next_to(new_lt, DOWN, buff=0)
        new_lt.shift(DOWN * (lt_height + 0.3))
        
        self.__scene.add(new_lt, reveal_mask)
        self.__scene.bring_to_front(reveal_mask)
        self.__scene.play(new_lt.animate.shift(UP * (lt_height + 0.3)), run_time=0.7, rate_func=custom_ease_out_cubic)
        self.__scene.remove(reveal_mask)
        self.__current_lower_third = new_lt

    def utils_lower_third_hide(self) -> None:
        if self.__current_lower_third is not None:
            lt = self.__current_lower_third
            lt_height = lt.height
            hide_mask = Rectangle(width=lt.width + 1.0, height=lt_height + 1.0, fill_color=self.__typo.bg(), fill_opacity=1, stroke_width=0).next_to(lt, DOWN, buff=0)
            self.__scene.add(hide_mask)
            self.__scene.bring_to_front(hide_mask)
            self.__scene.play(lt.animate.shift(DOWN * (lt_height + 0.3)), run_time=0.5, rate_func=smooth)
            self.__scene.remove(lt, hide_mask)
            self.__current_lower_third = None


class IntroOutro(IIntroOutro):
    def __init__(self, scene: Scene, typo: ITypography, tracker: IScreenTemplate):
        self.__scene = scene
        self.__typo = typo
        self.__tracker = tracker

    def __execute_masked_intro(self, title: str, line_color: str):
        title_mob = Text(title, font=self.__typo.font_ui(), font_size=42, color=self.__typo.color_white(), weight=BOLD)
        title_target_pos = UP * 0.6
        title_mob.move_to(title_target_pos)
        
        padding = 0.4
        accent_line = Line(
            start=LEFT * (title_mob.width / 2 + padding),
            end=RIGHT * (title_mob.width / 2 + padding),
            color=line_color,
            stroke_width=4
        ).next_to(title_mob, DOWN, buff=0.35)
        
        mask = Rectangle(width=config.frame_width, height=4.0, fill_color=self.__typo.bg(), fill_opacity=1, stroke_width=0).next_to(ORIGIN, DOWN, buff=0)
        title_mob.shift(DOWN * 1.5)
        
        self.__scene.add(title_mob, mask)
        self.__scene.bring_to_front(mask)
        
        self.__scene.play(title_mob.animate.move_to(title_target_pos), run_time=0.7, rate_func=custom_ease_out_cubic)
        self.__scene.play(GrowFromCenter(accent_line), run_time=0.4, rate_func=smooth)
        self.__scene.wait(3.3)
        
        self.__scene.bring_to_front(mask)
        self.__scene.play(Uncreate(accent_line), title_mob.animate.shift(DOWN * 1.5), run_time=0.6, rate_func=custom_ease_out_cubic)
        self.__scene.remove(title_mob, mask)

    def intro_lecture(self, title: str) -> None:
        # লেকচারের জন্য স্ট্যান্ডার্ড ব্লু পেডেস্টাল লাইন ইন্টারফেস
        self.__execute_masked_intro(title, self.__typo.color_blue())

    def intro_section(self, title: str) -> None:
        # মডিউল/সেকশনের জন্য প্রিমিয়াম গোল্ডেন-ইয়েলো পেডেস্টাল লাইন ইন্টারফেস
        self.__execute_masked_intro(title, self.__typo.color_yellow())

    def outro_lecture(self, next_topic: str) -> None:
        """Step 6: Code Submission & Outro (The Dopamine Hit)"""
        self.__tracker.screen_code_submission()
        
        # LeetCode প্ল্যাটফর্মের স্ক্রিন সিমুলেশন (Accepted পপ-আপ)
        accepted_box = Rectangle(width=5.0, height=1.4, fill_color="#1E293B", fill_opacity=0.95, stroke_color=self.__typo.color_milestone_green(), stroke_width=2.5)
        accepted_text = Text("Accepted", font=self.__typo.font_ui(), font_size=34, color=self.__typo.color_milestone_green(), weight=BOLD)
        stats_text = Text("Beats 100% of Runtime Users", font=self.__typo.font_code(), font_size=14, color=self.__typo.color_secondary())
        
        ui_contents = VGroup(accepted_text, stats_text).arrange(DOWN, buff=0.18)
        leetcode_ui = VGroup(accepted_box, ui_contents).move_to(ORIGIN)
        
        self.__scene.play(FadeIn(leetcode_ui, scale=0.92), run_time=0.5)
        self.__scene.wait(4.5) # শিক্ষক মুখের এন্ডিং ডায়ালগ দেবেন এই সময়

        # নো-সাউন্ড টাইটেল মাস্কিং/ফেড-ইন ট্রানজিশন
        next_topic_mob = Text(f"Next Topic: {next_topic}", font=self.__typo.font_ui(), font_size=38, color=self.__typo.color_white(), weight=BOLD)
        next_topic_mob.move_to(ORIGIN)
        
        self.__scene.play(
            FadeOut(leetcode_ui),
            FadeIn(next_topic_mob, shift=UP * 0.2),
            run_time=0.6
        )
        self.__scene.wait(3.0) # স্ক্রিনে ৩ সেকেন্ড ফিক্সড হোল্ড থাকবে

        # Smooth Fade to Black (0.5s)
        self.__scene.play(FadeOut(Group(*self.__scene.mobjects)), run_time=0.5)
        self.__scene.wait(0.2)

    def outro_section(self, section_title: str, challenges: list, next_module: str) -> None:
        """🏆 Integrated Milestone Outro Flow"""
        self.__tracker.screen_code_submission()
        self.__scene.wait(0.3)

        # গ্রিন কালার টাইটেল মাস্কিং রিভিল
        title_text = Text(f"🏆 SECTION COMPLETE: {section_title.upper()}", font=self.__typo.font_ui(), font_size=34, color=self.__typo.color_milestone_green(), weight=BOLD)
        title_text.move_to(UP * 1.3)
        
        mask = Rectangle(width=config.frame_width, height=3.5, fill_color=self.__typo.bg(), fill_opacity=1, stroke_width=0).next_to(UP * 0.2, DOWN, buff=0)
        title_text.shift(DOWN * 1.6)
        self.__scene.add(title_text, mask)
        self.__scene.bring_to_front(mask)
        
        self.__scene.play(title_text.animate.move_to(UP * 1.3), run_time=0.8, rate_func=custom_ease_out_cubic)
        self.__scene.remove(mask)
        self.__scene.wait(2.2) # Deep Ambient Achievement Swell সাউন্ডের সাথে টোটাল ৩ সেকেন্ড থাকবে

        # "The Blind Challenges" স্লেট ডাইনামিক পপ-আপ
        challenge_header = Text("💪 CHALLENGE YOURSELF (Check Resources to Solve)", font=self.__typo.font_ui(), font_size=18, color=self.__typo.color_yellow(), weight=BOLD)
        
        challenge_lines = VGroup(challenge_header)
        for idx, ch in enumerate(challenges, 1):
            ch_line = Text(f"Challenge {idx}: {ch}", font=self.__typo.font_code(), font_size=15, color=self.__typo.color_white())
            challenge_lines.add(ch_line)
            
        slate = challenge_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        slate.next_to(title_text, DOWN, buff=0.7).scale(0.95)
        
        self.__scene.play(FadeIn(slate, shift=UP * 0.3), run_time=0.6)
        self.__scene.wait(5.0) # শিক্ষক মুখে হোমওয়ার্কের কথা ব্যাখ্যা করবেন

        # পরবর্তী মডিউলের জন্য সাইলেন্ট ক্রস-ফেড ট্রানজিশন
        next_mod_mob = Text(f"Next Module: {next_module}", font=self.__typo.font_ui(), font_size=38, color=self.__typo.color_blue(), weight=BOLD)
        next_mod_mob.move_to(ORIGIN)
        
        self.__scene.play(
            FadeOut(slate),
            FadeOut(title_text),
            FadeIn(next_mod_mob, scale=1.03),
            run_time=0.8
        )
        self.__scene.wait(2.0) # ২ সেকেন্ড হোল্ড

        # Smooth Fade to Black (0.5s)
        self.__scene.play(FadeOut(Group(*self.__scene.mobjects)), run_time=0.5)
        self.__scene.wait(0.2)


# ═══════════════════════════════════════════════════════════════════
#  3. Full Production Environment Scenario Test
# ═══════════════════════════════════════════════════════════════════

class FullCourseTemplateDemo(Scene):
    def construct(self):
        # ডিপেন্ডেন্সি ইনজেকশন ও আর্কিটেকচার ইনিশিয়ালাইজেশন
        typo = Typography()
        self.camera.background_color = typo.bg()
        
        tracker = ScreenTemplate(self, typo)
        lower_third = LowerThird(self, typo)
        engine = IntroOutro(self, typo, tracker)

        # 🎬 ১. লেকচার ইনট্রো রান
        engine.intro_lecture("Find Middle Element of Linked List")

        # ⚪ ২. মেইন লেকচার ফেজ ও লোয়ার থার্ড ইউটিলিটি টেস্ট
        tracker.screen_statement()
        lower_third.utils_lower_third_show("Problem Understanding", "Linked List Node Analysis", "white")
        self.wait(1.5)

        # 🔴 ৩. অপটিমাল অ্যাপ্রোচ ফেজ ট্রানজিশন
        tracker.screen_optimal_approach()
        lower_third.utils_lower_third_show("Two-Pointer Architecture", "Time: O(N) · Space: O(1)", "yellow")
        self.wait(1.5)
        
        lower_third.utils_lower_third_hide()
        self.wait(0.5)

        # 💻 ৪. লেকচার আউট্রো ফ্লো টেস্ট (Step 6)
        engine.outro_lecture("Reverse a Linked List")


class MilestoneOutroDemo(Scene):
    def construct(self):
        typo = Typography()
        self.camera.background_color = typo.bg()
        
        tracker = ScreenTemplate(self, typo)
        engine = IntroOutro(self, typo, tracker)
        
        # ৫. মাইলস্টোন আউট্রো ফ্লো টেস্ট (Section End Automation)
        challenges = [
            "LeetCode 234 - Palindrome Linked List (Medium)",
            "LeetCode 25 - Reverse Nodes in k-Group (Hard)"
        ]
        engine.outro_section("Linked Lists", challenges, "Stacks & Queues")
