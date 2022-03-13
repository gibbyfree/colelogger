* store the last 20 
* if i press press backspace:
    * if i don't delete the entire token, save the deleted characters to a counted dict
        * unless i retype the character immediately after (false backspace)
    * if i delete the entire token and start from scratch, save the characters AND the word

detecting typo:
* if i backspace and retype the same set of characters right after, it was a false backspace / typo
* if i backspace and retype a different set of characters right afer, it was a typo -- save busted chars + the word itself
* if i backspace and there is a long pause let's call it a writing moment
    * also if i click and backspace