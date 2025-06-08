# auto_login.py

from playwright.sync_api import sync_playwright
import os
import time

STATE_FILE = "storage_state.json"
USERNAME = "IRVERTROLL"

def auto_login_mobile():
    with sync_playwright() as p:
        iphone = p.devices["iPhone 12"]
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**iphone)
        page = context.new_page()

        print("🔐 Iniciando sesión como móvil...")
        page.goto("https://www.cardmarket.com/es/Login", timeout=60000)

        try:
            page.fill('input[name="userName"]', USERNAME)
            page.fill('input[name="userPassword"]', PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_url("**/OnePiece", timeout=15000)  # Redirige al home
            print("✅ Login exitoso (móvil)")
        except Exception as e:
            print(f"❌ Error durante el login móvil: {e}")
        finally:
            context.storage_state(path=STATE_FILE)
            browser.close()

if __name__ == "__main__":
    auto_login_mobile()
