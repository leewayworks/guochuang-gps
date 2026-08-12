from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto((Path(__file__).parents[1] / "site" / "index.html").as_uri())
        page.wait_for_load_state("networkidle")
        assert "Guochuang GPS" in page.title()
        assert page.locator("h1").inner_text().strip()
        page.locator('[data-panel="gpa"]').first.click()
        page.wait_for_selector("#panel.open")
        assert "GPA" in page.locator("#panel-content").inner_text()
        page.locator(".panel-close").click()
        page.set_viewport_size({"width": 390, "height": 844})
        page.reload()
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(Path(__file__).parents[1] / "site" / "smoke-mobile.png"), full_page=True)
        assert not errors, errors
        print("web smoke passed")
        browser.close()


if __name__ == "__main__":
    main()
