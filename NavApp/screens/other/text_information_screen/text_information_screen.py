from kivymd.uix.screen import MDScreen


class TextInformationScreen(MDScreen):

    caller: str
    def goto_profile(self,btn):
        self.manager.goto_screen("pfs")

    def start_up_screen(self):
        # ovo se zove automatski na ulasku u ekran
        # ova funkcija treba populirati labele sa pravim tekstom ovisno otkud je funkcija pozvana
        # to će vam reći varijabla self.caller -> moguce vrijednosti (privacy -> pri, contact us -> con, points and levels - pal)
        # za sada napravite inicijalizaciju za privacy, učitajte tekst sa interneta nekako! (good luck)
        # SADRŽAJ MORA BITI SKROLABILAN - MDSCROLLVIEW, no nemojte slučajno da i skrola naslov i back button!!!
        pass