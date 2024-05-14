import kivy
from kivy import platform
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass

class RouteMapScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_view = None

    def open_webview(self, location_id):
        if platform != "android":
            return
        Clock.schedule_once(lambda dt: self.create_webview(location_id), 0.1)

    if platform == "android":
        from android.runnable import run_on_ui_thread

        @run_on_ui_thread
        def create_webview(self, location_id):
            if platform != "android":
                return

            from android import mActivity
            import android

            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')

            activity = mActivity
            #activity = autoclass('org.kivy.android.PythonActivity').mActivity
            webview = WebView(activity)
            webview.setWebContentsDebuggingEnabled(True)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.getSettings().setSupportZoom(True)
            webview.getSettings().setBuiltInZoomControls(True)
            webview.getSettings().setDisplayZoomControls(False)
            webview.getSettings().setBlockNetworkImage(False)
            webview.getSettings().setBlockNetworkLoads(False)
            webview.getSettings().setAllowUniversalAccessFromFileURLs(True)
            webview.getSettings().setAllowFileAccessFromFileURLs(True)
            webview.getSettings().setAllowFileAccess(True)

            wvc = WebViewClient()
            webview.setWebViewClient(wvc)
            # self.prev_view = mActivity.findViewById(android.R.id.content)
            # print(f"Prev view: {dir(self.prev_view)}")
            # print(f"Prev view: {self.prev_view}")
            activity.setContentView(webview)

            JSLocationDetails = autoclass("eu.greenstem.webview.JSLocationDetails")
            details = JSLocationDetails(self.manager.active_user.user_token, location_id)

            # webview.addJavascriptInterface(f"{self.manager.active_user.user_token}", "accessToken")
            webview.addJavascriptInterface(details, "locationDetails")
            webview.loadUrl("file:///android_asset/index.html")
            # Clock
            # print(f"User access token: {self.manager.active_user.user_token}")