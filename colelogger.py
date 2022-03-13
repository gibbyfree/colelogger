from pynput import keyboard
from queue import LifoQueue
from collections import Counter

prev_tokens = LifoQueue(20)  # past tokens we've written
prev_char = LifoQueue(50)  # past characters we've typed
curr_token = ""  # current token we're typing
core_modifiers = {keyboard.Key.space, keyboard.Key.backspace}  # important key events
bs_count = 0  # consecutive backspaces
bs_token = ""  # last characters we backspace
corrected_token = "" # correction to a backspace
bad_chars = Counter()
bad_words = {}


def print_report():
    print(bad_words)
    print(bad_chars)


def add_to_dicts():
    global curr_token, bs_token
    curr_token = curr_token[:len(curr_token) - len(bs_token)] + corrected_token
    
    if curr_token not in bad_words:
        bad_words[curr_token] = 1
    else:
        val = bad_words[curr_token]
        bad_words[curr_token] = val + 1
    
    bad_chars.update(bs_token)
    

def save_token():
    global prev_tokens, curr_token, bs_token, bs_count
    if (len(curr_token) > 0 and bs_count == 0):
        prev_tokens.put(curr_token)
        print("done token: " + curr_token)
        curr_token = ""
    elif (bs_count > 0):
        add_to_dicts()
        prev_tokens.put(curr_token)
        curr_token = ""
        bs_token = ""
        bs_count = 0


def proc_typo(key):
    global bs_count, curr_token, prev_char, bs_token
    bs_count += 1
    if (bs_count < len(curr_token)):  # we have not yet deleted the whole token
        try:
            bs_token += prev_char.get()
            print("bs token is: " + bs_token)
        except AttributeError:
            pass  # just ignore special characters
    elif (bs_count == len(curr_token)):
        bs_token = curr_token
        curr_token = ""
        print("deleted the whole token: " + bs_token)
        

def proc_standard_type(key):
    global prev_char, curr_token
    try:
        prev_char.put(key.char)
        curr_token += key.char
    except AttributeError:
        pass  # just ignore special characters
    

def proc_corrected_type(key):
    global prev_char, corrected_token
    try:
        prev_char.put(key.char)
        corrected_token += key.char
    except AttributeError:
        pass  # just ignore special characters


def on_press(key):
    global prev_char, curr_token, bs_count, bs_token
    if key not in core_modifiers:  # assume we are typing a word
        if (bs_count == 0):  # not typing after backspace
            proc_standard_type(key)
        else:
            proc_corrected_type(key)
    else:
        if key == keyboard.Key.space:  # save token
            save_token()
        if key == keyboard.Key.backspace:  # typo alert!
            proc_typo(key)


with keyboard.Listener(
        on_press=on_press) as listener:
    try:
        listener.join()
    except KeyboardInterrupt:
        print_report()
