from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="battleship_",
    password="secret-password"
)

if not cookies.ready():
    raise RuntimeError("Cookies not ready")