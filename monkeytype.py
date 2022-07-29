from selenium import webdriver
from selenium.webdriver.common.by import By as Selector
import time
from typer import Typer
from multiprocessing import Process, Queue, Value


def simulate_typing_in_browser(typer, input_textbox, text_to_type):

    for c in text_to_type:
        typer.simulate_typing_key_with_delay(c)
        input_textbox.send_keys(c)

    # input_textbox.send_keys(text_to_type)


def get_latest_words(browser, current_words, prefix_match_len = 3):
    # start_time = time.perf_counter()
    words_div = browser.find_element(by=Selector.CSS_SELECTOR, value="div#words")
    if not words_div:
        print("Could not find div#words")
        exit(1)

    # print(f"Find div#words: {time.perf_counter() - start_time}")
    raw_words_arr = words_div.text.split()
    # print(f"Batch find words split: {time.perf_counter() - start_time}")

    if len(current_words) == 0 or len(raw_words_arr) == 0:
        return raw_words_arr

    words_to_match = current_words[-prefix_match_len:] if len(current_words) >= prefix_match_len\
                                                       else current_words
    prefix_match_len = len(words_to_match)

    curr_idx = -1
    match_num = 0
    while curr_idx >= -len(raw_words_arr) and match_num != prefix_match_len:
        if raw_words_arr[curr_idx] == words_to_match[-1 - match_num]:
            match_num += 1

        curr_idx -= 1

    if match_num != prefix_match_len:
        # no match found, send the whole thing
        return raw_words_arr

    if curr_idx == -prefix_match_len - 1:
        # end of raw_words_arr matches end of current_words
        return []

    # print(f"Find words: {time.perf_counter() - start_time}")

    # Add empty string so it translates to an extra space when joining
    return [""] + raw_words_arr[curr_idx + prefix_match_len + 1:]



if __name__ == '__main__':
    browser = webdriver.Chrome()
    # Load browser
    browser.get("https://monkeytype.com")

    browser.implicitly_wait(60)  # wait upto a minute to resolve the html elements
    cookie_accept_all_button = browser.find_elements(by=Selector.CSS_SELECTOR, value="div.button.acceptAll")

    if len(cookie_accept_all_button) == 0:
        pass # do nothing if there isn't a cookie prompt
    elif len(cookie_accept_all_button) == 1:
        cookie_accept_all_button[0].click() # accept all cookies
    else:
        print(f"Invalid number of 'Accept All' buttons found: {len(cookie_accept_all_button)}")
        exit(1)

    time.sleep(5)

    inputs = browser.find_elements(by=Selector.CSS_SELECTOR, value="input#wordsInput")
    if len(inputs) != 1:
        print(f"Found invalid number of inputs: {len(inputs)}")
        exit(1)

    typer = Typer(1)

    words_arr = get_latest_words(browser, [])
    while len(words_arr) != 0:
        words = " ".join(words_arr)
        print(f"'{words}'")
        simulate_typing_in_browser(typer, inputs[0], words)
        words_arr = get_latest_words(browser, words_arr)
