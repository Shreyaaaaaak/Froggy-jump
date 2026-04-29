import curses
import time
import random

WIDTH       = 40
NUM_LANES   = 8
TOP_BANK    = 0
BOTTOM_BANK = TOP_BANK + 1 + NUM_LANES
LIVES_START = 3

LANE_CONFIGS = [
    (6,  -1, "▓"),
    (4,   1, "@"),
    (8,  -1, "▓"),
    (5,   1, "@"),
    (7,  -1, "▓"),
    (4,   1, "@"),
    (9,  -1, "▓"),
    (5,   1, "@"),
]

# ── Lane helpers ──────────────────────────────────────────────────────────────

def make_lanes(level):
    speed_mult = 1 + (level - 1) * 0.2
    lanes = []
    for speed, direction, obj in LANE_CONFIGS:
        pattern = [obj if random.random() < 0.4 else "~" for _ in range(WIDTH)]
        lanes.append({
            "pattern":   pattern,
            "offset":    0.0,
            "speed":     speed * speed_mult,
            "direction": direction,
        })
    return lanes

def update_lanes(lanes, dt):
    for lane in lanes:
        lane["offset"] += lane["speed"] * lane["direction"] * dt
        lane["offset"] %= WIDTH

def cell_at(lane, col):
    return lane["pattern"][int(col + lane["offset"]) % WIDTH]

def check_collision(lanes, frog_row, frog_col):
    if frog_row == TOP_BANK:    return "won"
    if frog_row == BOTTOM_BANK: return "safe"
    lane = lanes[frog_row - TOP_BANK - 1]
    for offset in range(3):
        if cell_at(lane, frog_col + offset) == "@":
            return "safe"
    return "dead"

# ── Drawing ───────────────────────────────────────────────────────────────────

def draw_board(stdscr, lanes, frog_row, frog_col, lives, score, level, message=""):
    stdscr.erase()

    stdscr.addstr(TOP_BANK, 0, "░" * WIDTH, curses.color_pair(2))
    stdscr.addstr(TOP_BANK, WIDTH // 2 - 4, " GOAL!! ", curses.color_pair(2))

    for i, lane in enumerate(lanes):
        for col in range(WIDTH):
            ch = cell_at(lane, col)
            color = (curses.color_pair(5) if ch == "▓"
                     else curses.color_pair(6) if ch == "@"
                     else curses.color_pair(1))
            try:
                stdscr.addch(TOP_BANK + 1 + i, col, ch, color)
            except curses.error:
                pass

    stdscr.addstr(BOTTOM_BANK, 0, "░" * WIDTH, curses.color_pair(2))
    stdscr.addstr(BOTTOM_BANK, WIDTH // 2 - 4, " START  ", curses.color_pair(2))
    stdscr.addstr(frog_row, frog_col, "())", curses.color_pair(4) | curses.A_BOLD)

    hearts = "♥ " * lives + "♡ " * (LIVES_START - lives)
    stdscr.addstr(BOTTOM_BANK + 1, 0,
        f" Lvl:{level}  Score:{score:04d}  {hearts}", curses.color_pair(3))
    stdscr.addstr(BOTTOM_BANK + 2, 0, " arrows=move  q=quit", curses.color_pair(3))
    if message:
        stdscr.addstr(BOTTOM_BANK + 3, 0, f" {message}",
            curses.color_pair(4) | curses.A_BOLD)
    stdscr.refresh()

# ── Screens ───────────────────────────────────────────────────────────────────

def show_screen(stdscr, lines, color):
    """Generic screen: draw lines, wait for SPACE or Q."""
    stdscr.erase()
    for i, line in enumerate(lines):
        try:
            stdscr.addstr(i, 0, line, curses.color_pair(color))
        except curses.error:
            pass
    stdscr.refresh()
    stdscr.nodelay(False)
    while True:
        k = stdscr.getch()
        if k == ord(' '): return True
        if k in (ord('q'), ord('Q')): return False

def splash_screen(stdscr):
    return show_screen(stdscr, [
        "",
        "   ╔══════════════════════════════════╗",
        "   ║      F R O G G Y   J U M P       ║",
        "   ║                                  ║",
        "   ║  Cross the river to score!       ║",
        "   ║                                  ║",
        "   ║  @  = lily pad  (safe)           ║",
        "   ║  ▓  = log       (deadly!)        ║",
        "   ║  ~  = water     (deadly!)        ║",
        "   ║                                  ║",
        "   ║    SPACE to start  |  Q to quit  ║",
        "   ╚══════════════════════════════════╝",
    ], color=4)

def level_screen(stdscr, level, score):
    return show_screen(stdscr, [
        "",
        "   ╔══════════════════════════════════╗",
        f"   ║       LEVEL {level-1} COMPLETE!           ║",
        "   ║                                  ║",
        f"   ║         Score: {score:04d}              ║",
        "   ║                                  ║",
        "   ║  Lanes are faster this time...   ║",
        "   ║                                  ║",
        "   ║      SPACE to continue           ║",
        "   ╚══════════════════════════════════╝",
    ], color=6)

def game_over_screen(stdscr, score, level):
    return show_screen(stdscr, [
        "",
        "   ╔══════════════════════════════════╗",
        "   ║           GAME  OVER             ║",
        "   ║                                  ║",
        f"   ║       Final score: {score:04d}          ║",
        f"   ║       Reached level: {level}            ║",
        "   ║                                  ║",
        "   ║  SPACE to play again | Q to quit ║",
        "   ╚══════════════════════════════════╝",
    ], color=5)

# ── Game session ──────────────────────────────────────────────────────────────

def play(stdscr, level, score):
    """
    Play one round. Returns (score, level, outcome).
    outcome is "won", "dead", or "quit".
    """
    stdscr.nodelay(True)
    lanes     = make_lanes(level)
    frog_row  = BOTTOM_BANK
    frog_col  = WIDTH // 2
    lives     = LIVES_START
    prev_time = time.time()

    while True:
        now, prev_time = time.time(), time.time()
        dt = now - prev_time + 0.016   # ~60fps floor

        key = stdscr.getch()
        if key in (ord('q'), ord('Q')):
            return score, level, "quit"

        if key == curses.KEY_UP:
            frog_row -= 1
        elif key == curses.KEY_DOWN:
            frog_row = min(BOTTOM_BANK, frog_row + 1)
        elif key == curses.KEY_LEFT:
            frog_col = max(0, frog_col - 1)
        elif key == curses.KEY_RIGHT:
            frog_col = min(WIDTH - 3, frog_col + 1)

        update_lanes(lanes, dt)
        result = check_collision(lanes, frog_row, frog_col)

        if result == "won":
            bonus  = 100 + level * 50
            score += bonus
            draw_board(stdscr, lanes, frog_row, frog_col,
                lives, score, level, f"+{bonus}!  Prepare for level {level+1}...")
            time.sleep(1.2)
            return score, level + 1, "won"

        elif result == "dead":
            lives -= 1
            msg = f"Ouch!  {lives} {'life' if lives==1 else 'lives'} left" if lives > 0 else "No more lives!"
            draw_board(stdscr, lanes, frog_row, frog_col, lives, score, level, msg)
            time.sleep(0.5)
            frog_row, frog_col = BOTTOM_BANK, WIDTH // 2
            if lives <= 0:
                return score, level, "dead"

        else:
            draw_board(stdscr, lanes, frog_row, frog_col, lives, score, level)

# ── Entry point ───────────────────────────────────────────────────────────────

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN,    -1)  # water
    curses.init_pair(2, curses.COLOR_GREEN,   -1)  # grass
    curses.init_pair(3, curses.COLOR_WHITE,   -1)  # HUD
    curses.init_pair(4, curses.COLOR_YELLOW,  -1)  # frog / splash
    curses.init_pair(5, curses.COLOR_RED,     -1)  # logs / game over
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # lily pads / level screen

    while True:
        if not splash_screen(stdscr):
            break                           # Q on splash = exit

        score, level = 0, 1

        while True:
            score, level, outcome = play(stdscr, level, score)

            if outcome == "quit":
                return                      # Q mid-game = exit immediately

            if outcome == "won":
                if not level_screen(stdscr, level, score):
                    return                  # Q on level screen = exit
                # SPACE → loop back into play() with new level

            else:  # "dead"
                if game_over_screen(stdscr, score, level):
                    break                   # SPACE = back to splash
                else:
                    return                  # Q = exit

curses.wrapper(main)