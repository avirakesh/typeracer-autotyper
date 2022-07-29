from selenium import webdriver
from selenium.webdriver.common.by import By as Selector
import time
from typer import Typer


def simulate_typing_in_browser(input_textbox, text_to_type):
    typer = Typer()

    for c in text_to_type:
        typer.simulate_typing_key_with_delay(c)
        input_textbox.send_keys(c)


if __name__ == '__main__':
    browser = webdriver.Chrome()
    # Load browser
    browser.get("https://play.typeracer.com?rt=2n4zxyut90")

    browser.implicitly_wait(60)  # waits upto a minute to resolve the html elements
    button = browser.find_elements(by=Selector.CSS_SELECTOR, value="a.raceAgainLink")

    if len(button) > 1:
        print("More than one start button found.")
        exit(0)

    button[0].click()
    time.sleep(4)  # Wait for all spans to load

    text_spans = browser.find_elements(by=Selector.CSS_SELECTOR, value="span[unselectable=\"on\"]")
    if len(text_spans) != 3:
        print(f"Expected 3 spans, found {len(text_spans)}")
        exit(0)
    text_div = text_spans[0].find_element(by=Selector.XPATH, value="..")

    text_to_type = text_div.text
    print(f"Text to type:\n{text_to_type}")

    input_textbox = browser.find_element(by=Selector.CSS_SELECTOR, value="input.txtInput:not(.txtInput-unfocused)")
    if not input_textbox:
        print("Could not find input text.")
        exit(0)

    simulate_typing_in_browser(input_textbox, text_to_type)
