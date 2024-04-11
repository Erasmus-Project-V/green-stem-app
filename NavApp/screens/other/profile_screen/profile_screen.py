from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen

from custom_widgets.miscellaneous.dialog_widget.dialog_widget import DialogWidget


class ProfileScreen(MDScreen):


    def start_up_screen(self):
        au = self.manager.active_user
        self.ids["uname"].text = au.get_user_attribute("username")
    def sign_out(self, button):
        self.sign_out_dialog = DialogWidget(title="Do you really want to sign out?",
                                            buttons=[
                                                MDFlatButton(
                                                    text="CANCEL",
                                                    theme_text_color="Custom",
                                                    text_color=self.blue_ref,
                                                    on_release = self.close_dialog

                                                ),
                                                MDFlatButton(
                                                    text="YES",
                                                    theme_text_color="Custom",
                                                    text_color=self.blue_ref,
                                                    on_release = self.sign_out_confirmed

                                                ),
                                            ],
                                            )
        self.sign_out_dialog.open()


    def close_dialog(self,*args):
        self.sign_out_dialog.dismiss()
    def sign_out_confirmed(self,*args):
        self.sign_out_dialog.dismiss()
        self.manager.active_user.erase_user_data()
        self.manager.goto_screen("lgn")

    def edit_profile(self,button):
        self.manager.goto_screen("pes")

    def edit_settings(self,button):
        self.manager.goto_screen("stg")

    def open_privacy(self,button):
        self.manager.goto_screen("tis")