from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
MDScreenManager:

    MDScreen:
        name: "screen A"
        md_bg_color: "lightblue"

        MDHeroFrom:
            id: hero_from
            tag: "hero"
            size_hint: None, None
            size: "120dp", "120dp"
            pos_hint: {"top": .98}
            x: 24
            MDRelativeLayout:
                size_hint: None, None
                size: hero_from.size
                Button:
                    background_color: 0, 0, 1, 1
                    on_press:
                        root.release_func(self.parent)
                FitImage:
                    size_hint: None, None
                    size: self.parent.size
                    allow_stretch: True
                    source: "/home/drswift/Projects/green-stem-app/NavApp/assets/images/roll_1.png"
                    radius: 24
                    opacity: 0.5
        MDRaisedButton:
            text: "Move Hero To Screen B"
            pos_hint: {"center_x": .5}
            y: "36dp"
            on_release:
                root.current_heroes = ["hero"]
                root.current = "screen B"

    MDScreen:
        name: "screen B"
        hero_to: hero_to
        md_bg_color: "cadetblue"

        MDHeroTo:
            id: hero_to
            tag: "hero"
            size_hint: None, None
            size: "220dp", "220dp"
            pos_hint: {"center_x": .5, "center_y": .5}

        MDRaisedButton:
            text: "Move Hero To Screen A"
            pos_hint: {"center_x": .5}
            y: "36dp"
            on_release:
                root.current_heroes = ["hero"]
                root.current = "screen A"
'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()