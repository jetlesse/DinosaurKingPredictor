from location import Location
from circle import Circle


# keeps track of the screen positions and where the important elements will be located on those screens
class Screen:
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_start = round(x_start)
        self.y_start = round(y_start)
        self.x_end = round(x_end)
        self.y_end = round(y_end)

        self.height = self.y_end - self.y_start
        self.width = self.x_end - self.x_start

    def start_point(self):
        return self.x_start, self.y_start

    def end_point(self):
        return self.x_end, self.y_end

    def screen_size(self):
        return self.width, self.height


def new_top_screen(start_pos, end_pos, attacks=3):
    return TopScreen(start_pos[0], start_pos[1], end_pos[0], end_pos[1], attacks)


def new_bottom_screen(start_pos, end_pos, attacks=3):
    return BottomScreen(start_pos[0], start_pos[1], end_pos[0], end_pos[1], attacks)


class TopScreen(Screen):
    def __init__(self, x_start, y_start, x_end, y_end, attacks=3):
        super().__init__(x_start, y_start, x_end, y_end)
        if attacks == 3:
            self.rock = Circle((self.x_start + self.width * 0.780, self.y_start + self.height * 0.327),
                               self.height * 0.096)
            self.paper = Circle((self.x_start + self.width * 0.897, self.y_start + self.height * 0.585),
                                self.height * 0.096)
            self.scissor = Circle((self.x_start + self.width * 0.668, self.y_start + self.height * 0.585),
                                  self.height * 0.096)
            self.fourth = Circle((0, 0), 0)

        elif attacks == 4:
            self.rock = (100, 100), 10
            self.paper = (110, 110), 10
            self.paper = (120, 120), 10
            self.fourth = (130, 130), 10

        self.my_attack = Circle((self.x_start + self.width * 0.315, self.y_start + self.height * 0.500),
                                self.height * 0.127)
        self.their_attack = Circle((self.x_start + self.width * 0.691, self.y_start + self.height * 0.500),
                                   self.height * 0.127)

        self.my_name = Location(self.x_start + self.width * 0.348, self.y_start + self.height * 0.838,
                                self.x_start + self.width * 0.975, self.y_start + self.height * 0.907)
        self.their_name = Location(self.x_start + self.width * 0.025, self.y_start + self.height * 0.087,
                                   self.x_start + self.width * 0.620, self.y_start + self.height * 0.155)

        self.text_box = Location(self.x_start + self.width * 0.025, self.y_start + self.height * 0.708,
                                 self.x_start + self.width * 0.975, self.y_start + self.height * 0.962)


class BottomScreen(Screen):
    def __init__(self, x_start, y_start, x_end, y_end, attacks=3):
        super().__init__(x_start, y_start, x_end, y_end)

        if attacks == 3:
            self.rock = Circle((self.x_start + self.width * 0.500, self.y_start + self.height * 0.229),
                               self.height * 0.123)
            self.paper = Circle((self.x_start + self.width * 0.647, self.y_start + self.height * 0.571),
                                self.height * 0.123)
            self.scissor = Circle((self.x_start + self.width * 0.353, self.y_start + self.height * 0.571),
                                  self.height * 0.123)
            self.fourth = Circle((0, 0), 0)

        elif attacks == 4:
            self.rock = (100, 100), 10
            self.paper = (110, 110), 10
            self.paper = (120, 120), 10
            self.fourth = (130, 130), 10

        self.text_box = Location(self.x_start + self.width * 0.025, self.y_start + self.height * 0.708,
                                 self.x_start + self.width * 0.975, self.y_start + self.height * 0.962)

        self.corner_trim = Location(self.x_start + self.width * 0.020, self.y_start + self.height * 0.020,
                                    self.x_start + self.width * 0.030, self.y_start + self.height * 0.030)

        self.arrow = Location(self.x_start + self.width * 0.900, self.y_start + self.height * 0.910,
                              self.x_start + self.width * 0.975, self.y_start + self.height * 0.962)
