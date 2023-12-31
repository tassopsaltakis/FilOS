import curses
import os

def text_editor(filename):
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Check if file exists and read it
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
    else:
        lines = ['']

    # Initial cursor position
    cursor_x = 0
    cursor_y = 0

    # Main loop
    while True:
        stdscr.clear()

        # Ensure cursor is within the boundaries of text
        cursor_x = max(0, min(cursor_x, len(lines[cursor_y]) - 1))
        cursor_y = max(0, min(cursor_y, len(lines) - 1))

        # Print lines to the screen
        height, width = stdscr.getmaxyx()
        for i, line in enumerate(lines):
            if i < height - 2:  # Reserve last two lines for control bar
                stdscr.addstr(i, 0, line)

        # Control bar at the bottom
        stdscr.addstr(height - 2, 0, '-' * width)  # Horizontal line
        controls = "CTRL+Q: Quit | CTRL+S: Save | Arrow Keys: Navigate"
        stdscr.addstr(height - 1, 0, controls)

        # Move cursor to position
        stdscr.move(min(cursor_y, height - 3), cursor_x)  # Adjust cursor position for control bar

        # Refresh to show the cursor
        stdscr.refresh()

        # Wait for user input
        ch = stdscr.getch()

        # Quitting (using CTRL+Q instead of just 'q' for similarity with Nano)
        if ch == 17:  # ASCII for CTRL+Q
            break

        # Handling Backspace
        elif ch == curses.KEY_BACKSPACE or ch == 127:
            if cursor_x > 0:
                lines[cursor_y] = lines[cursor_y][:cursor_x - 1] + lines[cursor_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y > 0:
                # Move up to the end of the previous line
                cursor_x = len(lines[cursor_y - 1]) - 1
                lines[cursor_y - 1] = lines[cursor_y - 1].strip() + lines[cursor_y]
                lines.pop(cursor_y)
                cursor_y -= 1

        # Handling Arrow Keys
        elif ch == curses.KEY_LEFT:
            cursor_x = max(0, cursor_x - 1)
        elif ch == curses.KEY_RIGHT:
            cursor_x = min(len(lines[cursor_y]) - 1, cursor_x + 1)
        elif ch == curses.KEY_UP:
            cursor_y = max(0, cursor_y - 1)
        elif ch == curses.KEY_DOWN:
            cursor_y = min(len(lines) - 1, cursor_y + 1)

        # Handling Enter Key
        elif ch == 10:  # Enter key is 10 in ASCII
            lines.insert(cursor_y + 1, lines[cursor_y][cursor_x:])
            lines[cursor_y] = lines[cursor_y][:cursor_x]
            cursor_y += 1
            cursor_x = 0

        # Handling Normal Character Input
        elif 32 <= ch <= 126:  # Printable characters
            lines[cursor_y] = lines[cursor_y][:cursor_x] + chr(ch) + lines[cursor_y][cursor_x:]
            cursor_x += 1

    # Cleanup and close
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    # Write back to file
    with open(filename, 'w') as file:
        file.writelines(lines)

if __name__ == '__main__':
    filename = input("Enter the filename to edit: ")
    text_editor(filename)
