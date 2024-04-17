from jnius import autoclass
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.widget import MDWidget
from android.runnable import run_on_ui_thread


class ActivityMapWidget(Widget):
    def __init__(self, **kwargs):
        super(ActivityMapWidget, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.create_webview(), 0.1)

    @run_on_ui_thread
    def create_webview(self, *args):
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        from android import mActivity

        activity = mActivity
#activity = autoclass('org.kivy.android.PythonActivity').mActivity
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        wvc = WebViewClient()
        webview.setWebViewClient(wvc)
        activity.setContentView(webview)
        webview.loadUrl("https://www.google.com")
