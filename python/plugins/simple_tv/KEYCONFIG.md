
# Keyconfig structure

The keyconfig.json assigns a incoming linux input_event (https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28) which comes from a remote control to a char or special key.

The program itself filters on event_type == 1 and value == 1, which is a key_event with key_down. Repeated key events are suppressed, so the key has to be pressed again for another char.

The config distingliush between codes with and without `isascii` been set or not. If not set, the code is handled as special key like cursor up or down, and its `key` value is the name of the special key

If `isascii` is set, its `key` value is used *as a whole lookop table!* like follows:

In the sample below, there a code of "2" and a key of "1234567890".

So when a code of 2 comes in, it's assigned to the first char of `key`, which is "1".

If now a code of 3 (= 2 +1 ) would come in, it would be assigned to the second char, which is the "2", and so on.

Which that a whole set of ascending codes can be handled in one statement, they dont have to be descripted all seperately by their own.




```
{
    "2": {
        "isascii": true,
        "key": "1234567890"
    },
    "14": {
        "key": "backspace"
    }
}
```