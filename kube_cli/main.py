from prompt_toolkit import (
    prompt,
    PromptSession
)

from prompt_toolkit.history import FileHistory

from prompt_toolkit.completion import (
    Completer,
    Completion
)

# actually, create a custom completion is good.

class MyCustomCompleter(Completer):

    def get_completions(self, document, complete_event):
        length = len(document.text)
        yield Completion('completion1', start_position=-length,
                        style='bg:ansiyellow fg:ansiblack')

        yield Completion('completion2', start_position=-length,
                        style='bg:ansiyellow fg:ansiwhite')


if __name__ == "__main__":
    session = PromptSession(history=FileHistory('~/.myhistory'))
    while True:
        try:

            content = session.prompt(">", completer=MyCustomCompleter(), complete_while_typing=True)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            print(f"You entered: {content}")

    print("exit..")

