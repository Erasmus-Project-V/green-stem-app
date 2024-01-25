from kivymd.uix.screen import MDScreen


class SignUpScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def create_new_user(self,button):
        print("Creating a new user")
        username = self.ids["new_user_name_text"].return_text()
        email = self.ids["new_email_text"].return_text()
        password = self.ids["new_password_text"].return_text()
        password_repeat = self.ids["new_password_repeat_text"].return_text()

        if "" in (email,password, username):
            print("Please input something!")
            return
        elif len(email) > 50 or len(password) > 50:
            print("email/password too long!")
            return
        if password != password_repeat:
            print("Passwords are not matching")
            return
        log, is_good = self.send_new_user(email,password)
        print(log)
        if is_good:
            self.manager.goto_screen("hme")
        
    def send_new_user(self,email,password):
        # šalje se email i password u backend te se onda dalje ide s tim
        return "login info recieved from backend",True
