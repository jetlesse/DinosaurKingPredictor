import math


class Circle:
    def __init__(self, center, radius):
        self.center = (int(center[0]), int(center[1]))
        self.radius = int(radius)

    def get_mp(self, idx):
        """
        get pixel that will be within the idx-th section of the MP bar
        :param idx: how much MP loss to check (0 means full MP, 3 means 3 MP used)
        :return: (x_pos, y_pos)
        """
        return int(self.center[0] + self.radius * math.sin((idx + 1.5) * math.pi / 6)),\
               int(self.center[1] + self.radius * math.cos((idx + 1.5) * math.pi / 6))

    def get_move_type(self, idx):
        """
        get pixel that is inside the MP bar. this should be the colour of the move
        :param idx: position on the circle for the pixel
        :return: (x_pos, y_pos)
        """
        return int(self.center[0] + self.radius * 0.72 * math.sin((idx + 1.5) * math.pi / 6)), \
               int(self.center[1] + self.radius * 0.72 * math.cos((idx + 1.5) * math.pi / 6))
