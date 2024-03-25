from kivy.animation import Animation
from kivy.clock import Clock
from kivy.gesture import Gesture, GestureStroke, GestureDatabase
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.gesturesurface import GestureSurface, GestureContainer
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import SlideTransition, FadeTransition
from kivy.multistroke import Recognizer, MultistrokeGesture, Candidate


class HomeScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.current_activity = 3

        # start up gestures
        self.gesture_locked = False
        self.recognizer = Recognizer()
        self.min_gesture_ratio = 0.3
        self.recognizer.import_gesture(filename="assets/gestures/gestures.kg")

        # start up activities
        self.activities = ["planinarenje", "hodanje", "trcanje", "bicikliranje", "rolanje"]
        self.image_base = "assets/images/home/home_*_1.png"
        self.current_image = self.image_base.replace("*", self.activities[2])

        # widget references
        self.image_swiper = None
        self.recognizer_surface = None
        self.first_image_container = None
        self.second_image_container = None
        self.start_button = None
        self.top_text_widget = None

        self.is_built = False
        self.event = Clock.schedule_once(self.further_build, 0)

    def further_build(self, dt):

        self.recognizer_surface: GestureSurface = self.ids["gesture_catcher"]
        self.recognizer_surface.bind(on_gesture_complete=self.handle_gesture_complete)

        self.image_swiper = self.ids["swipe_image"]
        self.first_image_container = self.ids["first_image_container"]
        self.second_image_container = self.ids["second_image_container"]
        self.start_button = self.ids["start_button"]
        self.top_text_widget = self.ids["top_text"]

        self.image_swiper.component_width = dp(self.manager.dimensions[0])
        self.image_swiper.encase_kwargs["width"] = dp(self.manager.dimensions[0]) / 3
        self.image_swiper.build_self(None)
        self.second_image_container.opacity = 0
        self.is_built = True

    def start_up_screen(self):
        if not self.is_built:
            self.event.cancel()
            self.further_build(0)
        self.set_up_user_data()

    def set_up_user_data(self):
        username = self.manager.active_user.get_user_attribute("username")
        if username:
            self.top_text_widget.text = f"Hello, {username}!"

    def handle_gesture_complete(self, surface, container: GestureContainer):
        if self.gesture_locked:
            return

        self.recognizer.recognize(Candidate(container.get_vectors(), skip_bounded=False, skip_invariant=True))
        self.direction, self.ratio = self.calculate_gesture_direction(container)

        self.recognizer.bind(on_search_complete=self.handle_recognition_complete)

    def calculate_gesture_direction(self, container):
        direction = int(container.get_vectors()[0][0][0] - container.get_vectors()[0][-1][0])
        ratio = abs(direction / self.recognizer_surface.width)
        direction = int(direction // abs(direction))
        return direction, ratio

    def animate_image(self):
        self.current_image = self.image_base.replace("*", self.activities[self.current_activity - 1])
        self.second_image_container.source = self.current_image
        move = 0.6 if self.direction == -1 else 0.4
        opacity_raise = Animation(opacity=1, pos_hint={"center_x": 0.5}, duration=1, t="in_cubic")
        opacity_lower = Animation(opacity=0, pos_hint={"center_x": move}, duration=.75, t="out_cubic")
        opacity_lower.bind(on_complete=self.realign)
        opacity_raise.bind(on_complete=self.change_image)
        opacity_raise.start(self.second_image_container)
        opacity_lower.start(self.first_image_container)

    def handle_recognition_complete(self, _, gesture):
        if gesture.best["name"] in ("left", "right") and self.ratio > self.min_gesture_ratio:
            if -0.5 <= self.image_swiper.scroll_x + 0.5 * self.direction <= 1.5:
                self.image_swiper.change_current(self.direction)
                self.current_activity = self.image_swiper.get_current()
                self.animate_image()

                self.start_button.button_disabled = True
                self.gesture_locked = True

    def realign(self, *args):
        self.first_image_container.pos_hint["center_x"] = 0.5

    def change_image(self, *args):
        self.first_image_container.source = self.current_image
        self.second_image_container.pos_hint["center_x"] = 0.5
        self.first_image_container.opacity = 1
        self.second_image_container.opacity = 0
        self.gesture_locked = False
        self.start_button.button_disabled = False

    def start_activity_clicked(self, btn):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = "left"
        self.manager.goto_screen("act")
        self.manager.transition = FadeTransition()

    def reset_images(self, a):
        self.start_button.button_disabled = False
        self.first_image_container.pos_hint["center_y"] = 0.5
        self.first_image_container.size_hint = (1.2, 1)
        self.second_image_container.pos_hint["center_y"] = 0.5
        self.second_image_container.size_hint = (1.2, 1)

    def get_current_activity(self):
        return self.current_activity
