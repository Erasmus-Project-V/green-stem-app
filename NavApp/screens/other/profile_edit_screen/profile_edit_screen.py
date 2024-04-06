from kivymd.uix.screen import MDScreen


class ProfileEditScreen(MDScreen):

    def start_up_screen(self, *args):
        user_manager = self.manager.active_user
        name = user_manager.get_user_attribute("username")
        age = user_manager.get_user_attribute("age")
        height = user_manager.get_user_attribute("height")
        weight = user_manager.get_user_attribute("weight")

        self.username_entry = self.ids["uname"]
        self.age_entry = self.ids["age"]
        self.weight_entry = self.ids["weight"]
        self.height_entry = self.ids["height"]
        for a in [self.username_entry, self.height_entry, self.weight_entry, self.age_entry]:
            c = a.ids["text_field"]
            c.hint_text_color_normal = self.blue_container
            c.text_color_normal = "white"
            c.text_color_focus = "white"
            c.font_name = self.sans_container
        self.username_entry.set_text(name)
        self.age_entry.set_text(str(age))
        self.weight_entry.set_text(str(weight) + " kg")
        self.height_entry.set_text(str(height) + " cm")

    def attempt_data_change(self):
        user_manager = self.manager.active_user
        user_manager.send_request()

    def failure(self):
        pass

    def success(self):
        pass

    def return_to_profile(self, button):
        self.manager.goto_screen("pfs")
