import multiprocessing

def run():
    books = [
        'pride-and-prejudice.txt',
        'heart-of-darkness.txt',
        'frankenstein.txt',
        'dracula.txt'
    ]

    queue = multiprocessing.Queue()
    # how process queue to make interprocess communication.

    print("Enqueuing...")
    for book in books:
        print(book)
        queue.put(book)

    print("\nDequeuing...")
    while not queue.empty():
        print(queue.get())


if __name__ == '__main__':
    run()