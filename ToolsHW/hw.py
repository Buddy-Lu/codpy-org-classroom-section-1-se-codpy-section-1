import sys
import webbrowser

VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def open_video():
    webbrowser.open(VIDEO_URL)


def input_math():
    while True:
        user_input = input("1 times 1 = ? ")
        if user_input == "exit":
            sys.exit()
        if int(user_input) == 1:
            open_video()
            break
        print("Wrong! Try again.")


input_math()
