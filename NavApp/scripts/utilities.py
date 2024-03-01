from PIL import Image
from PIL import ImageDraw, ImageChops


# find parent manager using while loop with rules

def find_manager(parent, name="manager"):
    try:
        while hasattr(parent, "parent"):
            parent = parent.parent
            if hasattr(parent, "manager"):
                break
    except AttributeError:
        print("error occured while trying to locate screen manager from top_menu_widget")
        return None
    return parent.manager if parent.manager.name == name else None


def thumbnail_generator():
    print("treba generisati sliku za onaj profile, tj croppat ju")
