from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

import re
import os
from kivy.utils import platform

import_list_kv = []
import_list_py = []


def py_import_gen(py_abs_path, name):
    class_name = "".join([element[0].upper() + element[1:] for element in name.split("_")])
    cwd = os.getcwd()
    rel_path = py_abs_path.removeprefix(cwd).replace("/", ".")
    import_string = "from " + rel_path[1:] + " import " + class_name
    return import_string


def build_importer():
    if not import_list_py:
        return
    print(import_list_py)
    root_path = os.getcwd().split("/")[:-1]
    rp = ""
    for p in root_path:
        rp += p + "/"
    with open(f"__gen__imports__.py", "w") as gpi:
        gpi.write(f"#Dynamically generated, listing: {len(import_list_py)} imports\n")
        for import_statement in import_list_py:
            gpi.write(import_statement + "\n")
        gpi.write(f"#End of imports\n")
        gpi.close()
        print("done")


def seek(cd):
    directories = os.listdir(cd)
    for dir0 in directories:
        if re.search("(_screen)|(_widget)", dir0):
            base = cd + "/" + dir0
            if not os.listdir(base):
                return
            base += "/" + dir0
            import_list_kv.append(base + ".kv")
            import_list_py.append(py_import_gen(base, dir0))

        else:
            seek(cd + "/" + dir0)


if __name__ == "__main__":
    seek(os.getcwd().removesuffix("scripts") + "screens")
    build_importer()
else:
    search_dir = os.getcwd()
    print(f"Starting from {os.getcwd() + '/' + __name__.replace('.', '/')}")
    print(os.getcwd() + "/screens")
    seek(search_dir + "/screens")
    seek(search_dir + "/custom_widgets")
    build_importer()
    cwd_len = len(os.getcwd())
    for elemenat in range(len(import_list_kv)):
        import_list_kv[elemenat] = import_list_kv[elemenat][cwd_len + 1:]