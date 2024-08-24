import copy

import cv2 as cv
from colours import get_colour, get_mp_colour
import capture

# state 1: textbox arrow and text box
# state 2: corner trim
# state 3: opponent's moves
# state 4: dino names
# state 5: your moves
# state 6: moves used


class Setup:
    def __init__(self, top_screen, bottom_screen, cfg, input_type):
        self.top_screen = top_screen
        self.bottom_screen = bottom_screen
        if input_type == "Live" and getattr(cfg, "window_name", None):
            self.cap = capture.WindowCapture(cfg.window_name, cfg.border_pixels, cfg.titlebar_pixels)
        elif input_type == "Recording" and getattr(cfg, "filename", None) and getattr(cfg, "start_time", None):
            self.cap = capture.VideoCapture(cfg.filename, cfg.fps)
            self.cap.jump_to(cfg.start_time)
        else:
            print("Missing required parameters for setup")
            exit(1)

        self.output = ""
        self.state = 0
        self.max_state = 6
        self.print_output = False
        self.stop = False
        self.pause = False
        self.complete_loop = False

    def change_state(self, value):
        if 0 < value <= self.max_state:
            self.state = value

    def run(self):
        """
        rearrange the x,y coordinates because opencv indexes the frame as x,y but the image array uses y,x
        :return:
        """
        while True:
            # last_time = time.time()
            # do not get new frame if user has paused playback, continue rest of logic
            if not self.pause:
                # Capture new frame
                base_frame = self.cap.next_frame()
            frame = copy.deepcopy(base_frame)
            self.output = ""

            match self.state:
                case 1:
                    """
                    box around all text
                    black dot off of the arrow, white dot in the middle of the arrow
                    console output (numbers not exact, last number is much larger than others):
                        State 1
                        Colour.TEXTBOX_BG
                        Colour.RED (or Colour.MP_RED)
                        [  4   4 196]
                    """
                    start_point = self.bottom_screen.arrow.start_point()
                    mid_point = (int((self.bottom_screen.arrow.start_point()[0] + self.bottom_screen.arrow.end_point()[0]) / 2),
                                int((self.bottom_screen.arrow.start_point()[1] + self.bottom_screen.arrow.end_point()[1]) / 2))
                    self.output += "\n" + "State 1"
                    self.output += "\n" + str(get_colour(frame[(start_point[1], start_point[0])]))
                    cv.circle(frame, start_point, 3, (0, 0, 0), -1)
                    self.output += "\n" + str(get_colour(frame[(mid_point[1], mid_point[0])]))
                    self.output += "\n" + str(frame[(mid_point[1], mid_point[0])])
                    cv.circle(frame, mid_point, 3, (255, 255, 255), -1)

                    cv.rectangle(frame, self.bottom_screen.text_box.start_point(),
                                 self.bottom_screen.text_box.end_point(), (0, 0, 0), 1)
                case 2:
                    """
                    black circle in the middle of light blue corner area
                    output:
                        State 2
                        Colour.MENU_CORNER_TRIM
                    """
                    self.output += "\n" + "State 2"
                    point = self.bottom_screen.corner_trim.start_point()
                    self.output += "\n" + str(get_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 3, (0, 0, 0), -1)
                case 3:
                    """
                    10 circles in the MP bars of each attack, should be as close to the middle of the bar as possible
                    dots are read counter clockwise from the bottom right.
                    if reading for a dot is Colour.None, the coordinates or radius of the circle needs to be adjusted
                    output:
                        State 3
                        Rock
                        Colour.RED
                        ...
                        Colour.GREEN
                        Paper
                        Colour.RED
                        ...
                        Colour.GREEN
                        Scissor
                        Colour.RED
                        ...
                        Colour.GREEN
                    """
                    self.output += "\n" + "State 3"
                    self.output += "\n" + "Rock"
                    point = self.top_screen.rock.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.rock.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    self.output += "\n" + "Paper"
                    point = self.top_screen.paper.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.paper.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    self.output += "\n" + "Scissor"
                    point = self.top_screen.scissor.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.top_screen.scissor.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    # if the coordinate is not 0, assume it is a valid position and display
                    if self.top_screen.fourth.center[0] != 0:
                        self.output += "\n" + "Fourth"
                        point = self.top_screen.fourth.get_mp(0)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(1)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(2)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(3)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(4)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(5)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(6)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(7)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(8)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.top_screen.fourth.get_mp(9)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                case 4:
                    """
                    white boxes surrounding all text for the names of your dinosaur and the opponent's dinosaur
                    """
                    cv.rectangle(frame, self.top_screen.my_name.start_point(), self.top_screen.my_name.end_point(), (255, 255, 255), 1)
                    cv.rectangle(frame, self.top_screen.their_name.start_point(), self.top_screen.their_name.end_point(), (255, 255, 255), 1)
                case 5:
                    """
                    10 circles in the MP bars of each attack, should be as close to the middle of the bar as possible
                    dots are read counter clockwise from the bottom right.
                    if reading for a dot is Colour.None, the coordinates or radius of the circle needs to be adjusted
                    output:
                        State 5
                        Rock
                        Colour.RED
                        ...
                        Colour.GREEN
                        Paper
                        Colour.RED
                        ...
                        Colour.GREEN
                        Scissor
                        Colour.RED
                        ...
                        Colour.GREEN
                    """
                    self.output += "\n" + "State 5"
                    self.output += "\n" + "Rock"
                    point = self.bottom_screen.rock.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.rock.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    self.output += "\n" + "Paper"
                    point = self.bottom_screen.paper.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.paper.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    self.output += "\n" + "Scissor"
                    point = self.bottom_screen.scissor.get_mp(0)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(1)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(2)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(3)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(4)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(5)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(6)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(7)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(8)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)
                    point = self.bottom_screen.scissor.get_mp(9)
                    self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                    cv.circle(frame, point, 2, (0, 0, 0), 1)

                    # if the coordinate is not 0, assume it is a valid position and display
                    if self.bottom_screen.fourth.center[0] != 0:
                        self.output += "\n" + "Fourth"
                        point = self.bottom_screen.fourth.get_mp(0)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(1)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(2)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(3)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(4)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(5)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(6)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(7)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(8)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                        point = self.bottom_screen.fourth.get_mp(9)
                        self.output += "\n" + str(get_mp_colour(frame[(point[1], point[0])]))
                        cv.circle(frame, point, 2, (0, 0, 0), 1)
                case 6:
                    """
                    black circles to the top right of the RPS icons for both attacks
                    output should say Colour.RED, Colour.BLUE or Colour.YELLOW
                    output (depends on attack used):
                        State 6
                        Colour.RED
                        Colour.YELLOW
                    """
                    self.output += "\n" + "State 6"
                    my_point = self.top_screen.my_attack.get_move_type(3)
                    self.output += "\n" + str(get_colour(frame[(my_point[1], my_point[0])]))
                    cv.circle(frame, self.top_screen.my_attack.get_move_type(3), 2, (0, 0, 0), 1)
                    their_point = self.top_screen.their_attack.get_move_type(3)
                    self.output += "\n" + str(get_colour(frame[(their_point[1], their_point[0])]))
                    cv.circle(frame, self.top_screen.their_attack.get_move_type(3), 2, (0, 0, 0), 1)

            cv.imshow('frame', frame)
            if self.print_output:
                self.print_output = False
                print(self.output)

            key_in = cv.waitKey(16) # ~60 fps
            if key_in == ord('q') or self.stop:
                break
