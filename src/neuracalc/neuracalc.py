import curses
import os

from neuracalc.exercise import RandomExercises


class NeuraCalcTUI:
    def __init__(self):
        self._width = 80
        self._stdscr = curses.initscr()
        self._stdscr = curses.newwin(1000, self._width)
        curses.start_color()
        curses.use_default_colors()
        curses.cbreak()
        self._stdscr.keypad(True)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        self._gen = RandomExercises()
        self._e = None
        self._errmsg = ""

        self.refresh_width()

    def refresh_width(self):
        self._width = os.get_terminal_size().columns
        if self._width > 120:
            self._width = 120

    def run(self):
        for e in self._gen:
            self._e = e
            self.draw_content()

        self.draw_results()

    def draw_content(self):
        while True:
            self.refresh_width()
            self._stdscr.clear()

            prompt = self._e.prompt

            header = f"NeuraCalc | {self._gen.i}/{self._gen.count}\n"
            self._stdscr.addstr(1, 0, header)
            self._stdscr.addstr(3, (self._width-len(prompt))//2,
                                prompt, curses.A_BOLD)

            answer_prompt = "Enter answer: "
            self._stdscr.addstr(5, 0, answer_prompt)

            if self._errmsg:
                self._stdscr.addstr(6, 0, self._errmsg, curses.color_pair(1))
                self._errmsg = ""

            self._stdscr.refresh()

            try:
                answer = self._stdscr.getstr(5, len(answer_prompt))
                self._e.check_answer(answer)
                break
            except ValueError as err:
                self._errmsg = str(err)
                continue

    def draw_results(self):
        self.refresh_width()
        self._stdscr.clear()

        results = self._gen.results
        for category, exercises in results.items():
            self._stdscr.addstr(f"{category}\n")

            for e in exercises:
                color = curses.color_pair(1)
                duration = round(e.duration, 2)

                if e.answer_correct:
                    color = curses.color_pair(2)
                    self._stdscr.addstr(
                        f"[OK] {e.solution}, took {duration}s\n", color
                    )
                else:
                    self._stdscr.addstr(
                        f"[NO] {e.solution}, answered '{e.user_answer}',"
                        f" took {duration}s\n",
                        color
                    )

        while self._stdscr.getkey() != curses.KEY_ENTER:
            pass

    def __del__(self):
        curses.endwin()


def main():
    tui = NeuraCalcTUI()
    tui.run()


if __name__ == "__main__":
    main()
