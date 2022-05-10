from settings import *

LEVELS = [
    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),
        (WIDTH / 2, HEIGHT - 190, 100, 80, "O"),
        (WIDTH * 3 / 4, HEIGHT - 205, 100, 180, "G"),

        # fourth variable passed in for mobs is ignored; used to be height
        (500, WIDTH - 500, HEIGHT - 100, 4, "M")
    ],
    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),
        (WIDTH / 2, HEIGHT - 190, 100, 80, "O"),
        (WIDTH * 3 / 4, HEIGHT - 205, 100, 180, "G"),
        (500, WIDTH - 500, HEIGHT - 100, 6, "M"),
        (WIDTH - 500, 500, HEIGHT - 100, 6, "M")
    ],
    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),
        (WIDTH / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 2 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 3 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 4 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 5 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH - 200, HEIGHT - 205, 100, 180, "G"),
        (500, WIDTH - 500, HEIGHT - 100, 5, "M")

    ],

    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),
        (WIDTH / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 2 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 3 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 4 / 7, HEIGHT - 100, 100, 80, "O"),
        (WIDTH * 5 / 7, HEIGHT - 100, 100, 80, "O"),
        (0, HEIGHT - 320, WIDTH, 40, "PO"),
        (WIDTH - 200, HEIGHT - 205, 100, 180, "G"),
        (500, WIDTH - 500, HEIGHT - 100, 5, "M")

    ],

    # level 5
    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),

        (WIDTH / 6, HEIGHT - 150, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 650, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 450, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 550, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 750, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 850, 100, 80, "O"),

        (WIDTH - 350, HEIGHT - 150, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 650, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 450, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 550, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 250, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 350, 100, 80, "O"),

        (WIDTH / 2 - 75, HEIGHT - 400, 150, 40, "P"),
        (WIDTH / 2 - 75, HEIGHT - 650, 150, 40, "P"),
        (WIDTH / 2 - 75, HEIGHT - 150, 150, 40, "P"),

        (WIDTH - 200, 150, 100, 180, "G"),
        (WIDTH - 210, 315, 120, 40, "P"),

        (500, WIDTH - 500, HEIGHT - 100, 6, "M"),
        (WIDTH - 500, 500, 100, 6, "M")
    ],

    [
        (0, HEIGHT - 40, WIDTH, 40, "P"),
        (0, 0, 40, HEIGHT, "P"),
        (0, 0, WIDTH, 40, "P"),
        (WIDTH - 40, 0, 40, HEIGHT, "P"),

        (WIDTH / 6, HEIGHT - 150, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 650, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 450, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 550, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 750, 100, 80, "O"),
        (WIDTH / 6, HEIGHT - 850, 100, 80, "O"),

        (WIDTH - 350, HEIGHT - 150, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 650, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 450, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 550, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 250, 100, 80, "O"),
        (WIDTH - 350, HEIGHT - 350, 100, 80, "O"),

        (WIDTH / 2 - 75, HEIGHT - 400, 150, 40, "P"),
        (WIDTH / 2 - 75, HEIGHT - 650, 150, 40, "P"),
        (WIDTH / 2 - 75, HEIGHT - 150, 150, 40, "P"),

        (WIDTH - 200, 150, 100, 180, "G"),
        (WIDTH - 210, 315, 120, 40, "P"),

        (500, WIDTH - 500, HEIGHT - 100, 6, "M"),
        (500, WIDTH - 500, HEIGHT - 200, 6, "M"),
        (WIDTH - 500, 500, 200, 6, "M"),
        (500, WIDTH - 500, HEIGHT - 300, 6, "M"),
        (WIDTH - 500, 500, 300, 6, "M"),
        (500, WIDTH - 500, HEIGHT - 400, 6, "M"),
        (WIDTH - 500, 500, 400, 6, "M"),
        (WIDTH - 500, 500, 100, 6, "M")
    ],
    ]