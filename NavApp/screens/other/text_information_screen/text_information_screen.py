import requests
from kivymd.uix.screen import MDScreen

class TextInformationScreen(MDScreen):

    caller: str
    fetched = False ## Dodavanje fetched varijable tako da se text samo jednom poziva sa servera a ne x puta...

    def goto_profile(self, btn):
        self.manager.goto_screen("pfs")

    def start_up_screen(self):
        if not TextInformationScreen.fetched: ## Provjeravanje statusa fetchanog texta
            try:
                url = "https://www.green-stem.eu/fitness/privacy-policy.tx"
                response = requests.get(url)
                if response.status_code == 200:
                    text = response.text
                    self.ids.privacy_paragraph.text = text
                    TextInformationScreen.fetched = True
                else:
                    print("Error fetching text from server! Status code:", response.status_code)
            except Exception as e: ## Error handeling 
                self.ids.privacy_paragraph.text = f"Error fetching text from server! {e}"
                print("Error fetching text from server! The file might not exist!", e)


        else: ## Debug koji printa ako je text već bio fetchan
            print("The text was already fetched!")
