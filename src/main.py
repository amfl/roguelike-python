from blessed import Terminal

def main():
    t = Terminal()
    print(t.enter_fullscreen())
    print("Hello world")

    with t.cbreak():
        inp = t.inkey()
    print('You pressed ' + repr(inp))

    # Commented because otherwise you can't see the above output
    # print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
