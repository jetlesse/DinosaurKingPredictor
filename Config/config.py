import screen
import yaml
import datetime
from location import Location
from circle import Circle


class VideoConfig:
    """
    gather battle data from a recorded video. specify in yaml which file to read and fps of the video.
    then specify the battles that are in the video to create multiple instances of Battle objects.
    """
    def __init__(self, file, fps, battles):
        self.file = file
        self.fps = fps
        self.battles = battles


def read_yaml_config(file_name):
    with open(file_name, "r") as file:
        cfg = yaml.load(file, Loader=yaml.Loader)
        return cfg


class Battle(yaml.YAMLObject):
    """
    represent instances of a battle in a video which will be viewed.
    specify the id of the opponent (see GameData/fights.csv).
    specify the start and end times (roughly) in the video.
    This will be translated into the frame to start and end watching the battle.
    You should be able to use the same id for multiple battles in one video file.
    """
    yaml_tag = '!Battle'

    def __init__(self, id, start_time, end_time):
        self.id = id
        self.start_time = start_time
        self.start_sec = -1
        self.end_time = end_time
        self.end_sec = -1

    def get_frame_nums(self, fps):
        """
        return the frame counts for the start and end of the battle.
        :param fps: fps of video file
        :return: Tuple (frame battle starts on, frame battle ends on)
        """
        start_delta = datetime.datetime.strptime(self.start_time, "%H:%M:%S") - datetime.datetime(1900, 1, 1)
        end_delta = datetime.datetime.strptime(self.end_time, "%H:%M:%S") - datetime.datetime(1900, 1, 1)

        return int(start_delta.total_seconds()) * fps, int(end_delta.total_seconds()) * fps


class ScreenConfig(yaml.YAMLObject):
    """
    set the position of the top and bottom screen in the image being read by the app.
    also specify the exact positions of certain elements if the defaults don't work for the user's setup
    """
    yaml_tag = '!Screen'

    def __init__(self, top_screen_start, top_screen_end, bottom_screen_end, bottom_screen_start):
        self.top_screen_start = top_screen_start
        self.top_screen_end = top_screen_end

        self.bottom_screen_end = bottom_screen_end
        self.bottom_screen_start = bottom_screen_start

    def get_screens(self, attacks=3):
        top_screen = screen.new_top_screen(self.top_screen_start[0], self.top_screen_end[0], attacks)

        bottom_screen = screen.new_bottom_screen(self.bottom_screen_start[0], self.bottom_screen_end[0], attacks)
        # if other configs are set in the file, set them as part of the screens, otherwise leave the defaults

        return top_screen, bottom_screen


class TopScreenConfig(yaml.YAMLObject):
    """
    create the top screen with positions and sizes of each element that exists on the top screen.
    """
    yaml_tag = '!TopScreen'

    def __init__(self, top_screen_start, top_screen_end, rock_x, rock_y, rock_r, paper_x, paper_y, paper_r,
                 scissor_x, scissor_y, scissor_r, my_attack_x, my_attack_y, my_attack_r,
                 their_attack_x, their_attack_y, their_attack_r, my_name_x1, my_name_x2, my_name_y1, my_name_y2,
                 their_name_x1, their_name_x2, their_name_y1, their_name_y2,
                 text_box_x1, text_box_x2, text_box_y1, text_box_y2,
                 fourth_x=None, fourth_y=None, fourth_r=None, attacks=3):
        self.top_screen_start = top_screen_start
        self.top_screen_end = top_screen_end
        self.rock_x = rock_x
        self.rock_y = rock_y
        self.rock_r = rock_r
        self.paper_x = paper_x
        self.paper_y = paper_y
        self.paper_r = paper_r
        self.scissor_x = scissor_x
        self.scissor_y = scissor_y
        self.scissor_r = scissor_r
        self.my_attack_x = my_attack_x
        self.my_attack_y = my_attack_y
        self.my_attack_r = my_attack_r
        self.their_attack_x = their_attack_x
        self.their_attack_y = their_attack_y
        self.their_attack_r = their_attack_r
        self.my_name_x1 = my_name_x1
        self.my_name_x2 = my_name_x2
        self.my_name_y1 = my_name_y1
        self.my_name_y2 = my_name_y2
        self.their_name_x1 = their_name_x1
        self.their_name_x2 = their_name_x2
        self.their_name_y1 = their_name_y1
        self.their_name_y2 = their_name_y2
        self.text_box_x1 = text_box_x1
        self.text_box_x2 = text_box_x2
        self.text_box_y1 = text_box_y1
        self.text_box_y2 = text_box_y2
        self.fourth_x = fourth_x
        self.fourth_y = fourth_y
        self.fourth_r = fourth_r
        self.attacks = attacks

    def get_screen(self):
        top_screen = screen.new_top_screen(self.top_screen_start[0], self.top_screen_end[0], self.attacks)
        top_screen.rock = Circle((self.rock_x, self.rock_y), self.rock_r)
        top_screen.paper = Circle((self.paper_x, self.paper_y), self.paper_r)
        top_screen.scissor = Circle((self.scissor_x, self.scissor_y), self.scissor_r)
        if self.attacks == 4:
            top_screen.fourth = Circle((self.fourth_x, self.fourth_y), self.fourth_r)

        top_screen.my_attack = Circle((self.my_attack_x, self.my_attack_y), self.my_attack_r)
        top_screen.their_attack = Circle((self.their_attack_x, self.their_attack_y), self.their_attack_r)

        top_screen.my_name = Location(self.my_name_x1, self.my_name_y1, self.my_name_x2, self.my_name_y2)
        top_screen.their_name = Location(self.their_name_x1, self.their_name_y1, self.their_name_x2, self.their_name_y2)
        top_screen.text_box = Location(self.text_box_x1, self.text_box_y1, self.text_box_x2, self.text_box_y2)
        return top_screen


class BottomScreenConfig(yaml.YAMLObject):
    """
    create the bottom screen with positions and sizes of each element that exists on the top screen.
    """
    yaml_tag = '!BottomScreen'

    def __init__(self, bottom_screen_start, bottom_screen_end, rock_x, rock_y, rock_r, paper_x, paper_y, paper_r,
                 scissor_x, scissor_y, scissor_r, text_box_x1, text_box_x2, text_box_y1, text_box_y2,
                 corner_trim_x1, corner_trim_x2, corner_trim_y1, corner_trim_y2,
                 arrow_x1, arrow_x2, arrow_y1, arrow_y2, fourth_x=None, fourth_y=None, fourth_r=None, attacks=3):
        self.bottom_screen_start = bottom_screen_start
        self.bottom_screen_end = bottom_screen_end
        self.rock_x = rock_x
        self.rock_y = rock_y
        self.rock_r = rock_r
        self.paper_x = paper_x
        self.paper_y = paper_y
        self.paper_r = paper_r
        self.scissor_x = scissor_x
        self.scissor_y = scissor_y
        self.scissor_r = scissor_r
        self.text_box_x1 = text_box_x1
        self.text_box_x2 = text_box_x2
        self.text_box_y1 = text_box_y1
        self.text_box_y2 = text_box_y2
        self.corner_trim_x1 = corner_trim_x1
        self.corner_trim_x2 = corner_trim_x2
        self.corner_trim_y1 = corner_trim_y1
        self.corner_trim_y2 = corner_trim_y2
        self.arrow_x1 = arrow_x1
        self.arrow_x2 = arrow_x2
        self.arrow_y1 = arrow_y1
        self.arrow_y2 = arrow_y2
        self.fourth_x = fourth_x
        self.fourth_y = fourth_y
        self.fourth_r = fourth_r
        self.attacks = attacks

    def get_screen(self):
        bottom_screen = screen.new_top_screen(self.bottom_screen_start[0], self.bottom_screen_end[0], self.attacks)
        bottom_screen.rock = Circle((self.rock_x, self.rock_y), self.rock_r)
        bottom_screen.paper = Circle((self.paper_x, self.paper_y), self.paper_r)
        bottom_screen.scissor = Circle((self.scissor_x, self.scissor_y), self.scissor_r)
        if self.attacks == 4:
            bottom_screen.fourth = Circle((self.fourth_x, self.fourth_y), self.fourth_r)

        bottom_screen.text_box = Location(self.text_box_x1, self.text_box_y1, self.text_box_x2, self.text_box_y2)
        bottom_screen.corner_trim = Location(self.corner_trim_x1, self.corner_trim_y1, self.corner_trim_x2, self.corner_trim_y2)
        bottom_screen.arrow = Location(self.arrow_x1, self.arrow_y1, self.arrow_x2, self.arrow_y2)
        return bottom_screen


class GeneralConfig(yaml.YAMLObject):
    yaml_tag = '!General'

    def __init__(self, my_dino=None, show_screen=False, filename="", window_name="", fps=60, start_time="0:00:00", save=True):
        self.my_dino = my_dino
        self.show_screen = show_screen
        self.filename = filename
        self.window_name = window_name
        self.fps = fps
        self.save = save
        self.start_time = start_time
