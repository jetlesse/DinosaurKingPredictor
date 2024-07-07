# object to save locations of the screen elements we want to see
class Location:
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

