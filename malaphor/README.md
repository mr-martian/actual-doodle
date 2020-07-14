# Basic Malaphor Generator

It takes an input idiom, and using a list of idioms it replaces one random word in the input idiom. The word is chosen based on the Apertium morph analysis.

## How to Use
- `pip install -r requirements.txt`
- Make sure you have apertium and apertium-eng, build it (or install with packaging)
- If the path to -eng happens to be `../../apertium-eng`, you don't need to do anything
- Otherwise, specify it as the argument to `./malaphor`, or set it as the env var `APERTIUM_ENG` (argument takes precedence)
- If -eng was installed with packaging, use `installed` instead of a path
- `echo "Hit the nail on the head" | ./malaphor` or `./malaphor < input_file.txt`. Give only one idiom as input.
- Enjoy this stupid little useless tool! :)
