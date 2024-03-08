# green-stem-app

molim vas iz dna duše klonirajte si ovaj repo
i skinite intellij idea ultimate na svoja 
kućna računala kako bi mogli biti standardizirani

### Sadržaj
1. Requirements
<br>
2. Definicije
<br>
3. Metodologija
<br>




## Requirements:
Python 3.11 or newer
<br>
KivyMD 1.2.0
<br>
requests
<br>
os
<br>
time
<br>
Pillow
<br>
webbrowser
<br>
time
<br>

<br>

## Definicije
### scripts:
<p>
imports.py: 
modul za generaciju importa svih zasebnih ekrana/widgeta
u smislenom redoslijedu, ne prčkati. Da bi radilo
svi ekrani moraju poštovati metodologiju navedenu
u Metodologija/Novi ekrani/widgeti
<br>
utilities.py:
Korisne stvari u smislu kivy-a
find_manager(start) -> pronalazi glavni screen manager iz
bilo kojeg dijela projekta

<br>
Navodnici: Dvostruki!
<br>
</p>

## Metodologija
<p>
Općenito:
<br>
Moduli: mala slova, underscores 
<br>
Navodnici: Dvostruki!
<br>
Svi schedulani eventi sa Clock metodom
se po defaultu gase pri promjeni ekrana,
radi spasenja jadnog cpu-a, pale se 
na ulazu u screen - treba opisati metode
koje to actually rade though (napravljene su)
</p>

<p>
Skripte:
<br>

</p>
