package eu.greenstem.webview;

import android.webkit.JavascriptInterface;

public class JSLocationDetails {

    private String accessToken;
    private String locationId;

    public JSLocationDetails(String accessToken, String locationId) {
        this.accessToken = accessToken;
        this.locationId = locationId;
    }

    @JavascriptInterface
    public String getAccessToken() {
        return accessToken;
    }

    public void setAccessToken(String accessToken) {
        this.accessToken = accessToken;
    }

    @JavascriptInterface
    public String getLocationId() {
        return locationId;
    }

    public void setLocationId(String locationId) {
        this.locationId = locationId;
    }
}
