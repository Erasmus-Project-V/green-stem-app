from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView


class SwipeableImageWidget(ScrollView):
    source: StringProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
