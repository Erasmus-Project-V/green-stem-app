from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder

import re
import os

import_list_kv = []
import_list_py = []

# might be buggy
search_dir = "NavApp/screens"

def py_import_gen(py_abs_path, name):
    class_name = "".join([element[0].upper() + element[1:] for element in name.split("_")])
    cwd = os.getcwd()
    last = cwd.split("\\")[-1]
    cwd = cwd.removesuffix(last)
    rel_path = py_abs_path.removeprefix(cwd).replace("\\", ".")
    import_string = "from " + rel_path + " import " + class_name
    return import_string


def build_importer():
    if not import_list_py:
        return
    print(import_list_py)

    with open("scripts/__gen__imports__.py","w") as gpi:
        gpi.write(f"#Dynamically generated, listing: {len(import_list_py)} imports\n")
        for import_statement in import_list_py:
            gpi.write(import_statement+"\n")
        gpi.write(f"#End of imports\n")
        gpi.close()
        print("done")

def seek(cd):
    directories = os.listdir(cd)
    for dir in directories:
        if re.search("(_screen)|(_widget)", dir):
            base = cd + "\\" + dir
            if not os.listdir(base):
                return
            base += "\\" + dir
            import_list_kv.append(base + ".kv")
            import_list_py.append(py_import_gen(base, dir))

        else:
            seek(cd + "\\" + dir)


if __name__ == "__main__":
    seek(os.getcwd().removesuffix("scripts") + "screens")
    build_importer()
else:
    search_dir = os.getcwd()
    print(f"Starting from {os.getcwd() + __name__}")
    print(os.getcwd() + "\\screens")
    seek(search_dir+ "\\screens")
    seek(search_dir + "\\custom_widgets")
    build_importer()

