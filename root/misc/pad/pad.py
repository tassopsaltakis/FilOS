import os
import sys

class Pad:
    def __init__(self, filename):
        self.filename = filename
        self.content = ''
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.content = file.read()

    def run(self):
        print("Welcome to Pad! A simple text editor.")
        print("Type and edit the text. Type ':wq' to save and exit.")
        print("Type ':q' to exit without saving.")
        print("-------------------------------------------------")
        print(self.content)  # Print the current content of the file

        # Text Editing Loop
        while True:
            user_input = input()
            if user_input == ':wq':
                self.save_and_exit()
                break
            elif user_input == ':q':
                break
            else:
                self.content += user_input + '\n'  # Add new text to content

    def save_and_exit(self):
        """Save the current content to the file and exit."""
        with open(self.filename, 'w') as file:
            file.write(self.content)
        print(f"File '{self.filename}' saved. Exiting Pad...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pad filename")
    else:
        filename = sys.argv[1]
        pad = Pad(filename)
        pad.run()
