# Basic Malaphor Generator

It takes an input idiom, and using a list of idioms it replaces one random word in the input idiom. The word is chosen based on the Apertium morph analysis.

## How to Use
- `pip install -r requirements.txt`
- Make sure you have apertium and apertium-eng, build it, and put the path to it in the `malaphor` executable.
- `echo "Hit the nail on the head" | ./malaphor` or `./malaphor < input_file.txt`. Give only one idiom as input.
- Enjoy this stupid little useless tool! :)
