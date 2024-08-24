import csv
import os.path

import cv2
import cv2 as cv
from turn import Turn, new_turn
from colours import Colour, get_colour, get_mp_colour_fuzzy, get_move_colour_fuzzy
from GameData.StringConversion.dino_names import get_actual_dino_name
from GameData.StringConversion.sayings import get_actual_saying
from GameData import fights
import capture
import pytesseract

data_folder = 'TurnData/'
custom_config = r'-c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-.,?! " --oem 3  --psm 6'


def surrounding_pixels(frame, pixel):
    """
    gets a list of BGR values for the 3x3 pixels around the input pixel. Index 4 is
    the original pixel. Assumes that pixels exist on every side of the input pixel.

    :param frame: list of pixels given by Capture
    :param pixel: tuple (x_pos, y_pos) for the location of the pixel
    :return: list of BGR values for the 3x3 pixels around the input pixel
    """
    return [
        frame[pixel[1]-1, pixel[0]-1],
        frame[pixel[1],   pixel[0]-1],
        frame[pixel[1]+1, pixel[0]-1],
        frame[pixel[1]-1, pixel[0]],
        frame[pixel[1],   pixel[0]],
        frame[pixel[1]+1, pixel[0]],
        frame[pixel[1]-1, pixel[0]+1],
        frame[pixel[1],   pixel[0]+1],
        frame[pixel[1]+1, pixel[0]+1]
    ]


class Engine:
    def __init__(self, top_screen, bottom_screen):
        self.save = True
        self.player = next((x for x in fights.fights if x.id == "0000"), None)
        if self.player:
            self.player.read_dino_file()

        self.turn_state = 0
        self.turn = Turn()
        self.top_screen = top_screen
        self.bottom_screen = bottom_screen
        self.battle = None
        self.opponent = None
        self.stop = False # end the loop from outside the Engine class

        self.classifier = None
        self.prediction = None

    def run_video(self, battle, cfg):
        """
        run through frames of a video stream for a battle and gather the turn data for each turn

        :param battle: config for the battle to analyze
        :param cfg: a GeneralConfig object. Properties can be used to set or optimize execution
        :return: None
        """
        self.battle = battle
        self.opponent = next((x for x in fights.fights if x.id == str(battle.id)), None)
        if self.opponent:
            self.opponent.read_all_files()

        if cfg.save and self.opponent:
            if not os.path.exists(self.opponent.get_turn_file()):
                with open(self.opponent.get_turn_file(), "w") as f:
                    f.write("saying,my_last_move,their_last_move,my_rock,my_paper,my_scissor,"
                            "their_rock,their_paper,their_scissor,my_dino,their_dino,their_move\n")

        cap = capture.VideoCapture(cfg.filename, cfg.fps)

        self.turn_state = 0
        self.turn = Turn()
        cap.jump_to(battle.start_time)
        for i in range(cap.time_to_frame(battle.end_time) - cap.time_to_frame(battle.start_time)):
            # Capture frame-by-frame
            frame = cap.next_frame()

            self.process_frame(frame, cfg)

            cv.imshow('frame', frame)
            key_in = cv.waitKey(1) # 0.001 sec between frames is possible on video file without showing screen
            if key_in == ord('q'):
                break

    async def run_window(self, fight, cfg):
        """
        capture the screen in real time and gather turn data

        :param fight: Fight object.
        :param cfg: a GeneralConfig object. Properties can be used to set or optimize execution
        :return: None
        """
        self.stop = False
        self.opponent = fight
        self.opponent.read_all_files()

        if cfg.save and self.opponent:
            if not os.path.exists(self.opponent.get_turn_file()):
                with open(self.opponent.get_turn_file(), "w") as f:
                    f.write("saying,my_last_move,their_last_move,my_rock,my_paper,my_scissor,"
                            "their_rock,their_paper,their_scissor,my_dino,their_dino,their_move\n")

        cap = capture.WindowCapture(cfg.window_name, cfg.border_pixels, cfg.titlebar_pixels)

        self.classifier = fight.load_classifier()
        self.turn_state = 0
        self.turn = Turn()
        n_errs = 0
        while not self.stop:
            # Capture screenshot
            try:
                frame = cap.next_frame()
            except:
                print("error reading frame")
                n_errs += 1
                if n_errs >= 10:
                    return
                continue

            n_errs = 0
            self.process_frame(frame, cfg)

            if cfg.show_screen:
                cv.imshow('frame', frame)
            key_in = cv.waitKey(1) # min wait allowed by cv is 0.001 seconds
            if key_in == ord('q'):
                break
        return

    def process_frame(self, frame, cfg):
        """
        Process a single frame, agnostic to how the frame was obtained

        :param frame: a single frame including both the top and bottom screen. (BGR)
        :param cfg: a GeneralConfig object. Properties can be used to set or optimize execution
        :return: None
        """
        match self.turn_state:
            case 0:
                # only at the beginning of the fight, the opponent's move is shown before the first saying
                # this prevents catching text before the fight as the saying
                rock = self.top_screen.rock.get_mp(0)
                paper = self.top_screen.paper.get_mp(0)
                scissor = self.top_screen.scissor.get_mp(0)
                fourth = self.top_screen.fourth.get_mp(0)

                if get_mp_colour_fuzzy(surrounding_pixels(frame, rock)) in [Colour.MP_GREEN, Colour.MP_RED] and\
                        get_mp_colour_fuzzy(surrounding_pixels(frame, paper)) in [Colour.MP_GREEN, Colour.MP_RED] and\
                        get_mp_colour_fuzzy(surrounding_pixels(frame, scissor)) in [Colour.MP_GREEN, Colour.MP_RED] and\
                        (self.opponent.number_of_moves()[1] == 3 or
                            get_mp_colour_fuzzy(surrounding_pixels(frame, fourth)) in [Colour.MP_GREEN, Colour.MP_RED, Colour.NONE]):
                    self.turn_state = 1
            case 1:
                # reset last prediction
                self.prediction = None
                # try to find the continue arrow on the text box
                # its colour is very different from the box background
                start_point = (self.bottom_screen.arrow.start_point()[1], self.bottom_screen.arrow.start_point()[0])
                mid_point = (int((self.bottom_screen.arrow.start_point()[1] + self.bottom_screen.arrow.end_point()[1]) / 2),
                             int((self.bottom_screen.arrow.start_point()[0] + self.bottom_screen.arrow.end_point()[0]) / 2))
                if (get_colour(frame[start_point]) == Colour.TEXTBOX_BG and
                        frame[mid_point][2] > frame[mid_point][0] + 50 and
                        frame[mid_point][2] > frame[mid_point][1] + 50):
                    col = frame[start_point]
                    cv.rectangle(frame, self.bottom_screen.arrow.start_point(), self.bottom_screen.arrow.end_point(),
                                 (int(col[0]), int(col[1]), int(col[2])), -1)

                    text_box = frame[self.bottom_screen.text_box.start_point()[1]:self.bottom_screen.text_box.end_point()[1],
                                     self.bottom_screen.text_box.start_point()[0]:self.bottom_screen.text_box.end_point()[0]]
                    # not sure if this does anything.
                    img_rgb = cv2.cvtColor(text_box, cv2.COLOR_BGR2RGB)
                    result = pytesseract.image_to_string(img_rgb, config=custom_config).strip().lower().replace("\n", " ")
                    match = get_actual_saying(self.opponent.sayings, result)
                    print(match)
                    index = self.opponent.sayings.index(match)
                    self.turn.saying = index
                    # set the text in the turn, possibly async
                    self.turn_state = 2
                elif (get_colour(frame[self.bottom_screen.corner_trim.start_point()[1],
                                       self.bottom_screen.corner_trim.start_point()[0]]) == Colour.MENU_CORNER_TRIM):
                    # there is no saying this turn
                    self.turn_state = 2
            case 2:
                # get their MP values
                if self.opponent.number_of_moves()[1] == 3:
                    their_MP = [0, 0, 0]
                    for i in range(10):
                        point = self.top_screen.rock.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[0] = i + 1
                        point = self.top_screen.paper.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[1] = i + 1
                        point = self.top_screen.scissor.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[2] = i + 1
                else:
                    their_MP = [0, 0, 0, 0]
                    for i in range(10):
                        point = self.top_screen.rock.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[0] = i + 1
                        point = self.top_screen.paper.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[1] = i + 1
                        point = self.top_screen.scissor.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[2] = i + 1
                        point = self.top_screen.fourth.get_mp(i)
                        if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                            their_MP[3] = i + 1

                self.turn.their_mp_levels = their_MP
                if self.opponent.number_of_moves()[0] == 3:
                    self.turn.my_mp_levels = [0, 0, 0]
                else:
                    self.turn.my_mp_levels = [0, 0, 0, 0]
                self.turn_state = 3
            case 3:
                if cfg.my_dino:
                    # don't read my dino name, set based on config
                    result = cfg.my_dino
                else:
                    # read text and save into turn
                    my_dino = frame[self.top_screen.my_name.start_point()[1]:self.top_screen.my_name.end_point()[1],
                                    self.top_screen.my_name.start_point()[0]:self.top_screen.my_name.end_point()[0]]

                    result = pytesseract.image_to_string(my_dino, config=custom_config).strip()
                    result = get_actual_dino_name(self.player.dinos, result)
                    print(result)

                result = self.player.dinos.index(result)
                self.turn.my_dino = result

                self.turn_state = 4
            case 4:
                their_dino = frame[self.top_screen.their_name.start_point()[1]:self.top_screen.their_name.end_point()[1],
                                   self.top_screen.their_name.start_point()[0]:self.top_screen.their_name.end_point()[0]]

                result = pytesseract.image_to_string(their_dino, config=custom_config).strip()
                result = get_actual_dino_name(self.opponent.dinos, result)
                print(result)
                result = self.opponent.dinos.index(result)
                if self.turn.their_dino != result:
                    self.turn.my_last_move = 0
                    self.turn.their_last_move = 0
                self.turn.their_dino = result

                self.turn_state = 5
            case 5:
                # run the classifier for initial prediction
                if self.classifier:
                    self.prediction = self.classifier.predict_proba([self.turn.to_csv(self.opponent.number_of_moves())[:-1]])
                self.turn_state = 6
            case 6:
                # wait until you can see all your MP meters, then get MP levels
                if get_mp_colour_fuzzy(surrounding_pixels(frame, self.bottom_screen.rock.get_mp(5)))\
                        in [Colour.MP_GREEN, Colour.MP_RED] and\
                    get_mp_colour_fuzzy(surrounding_pixels(frame, self.bottom_screen.paper.get_mp(2)))\
                        in [Colour.MP_GREEN, Colour.MP_RED] and\
                    get_mp_colour_fuzzy(surrounding_pixels(frame, self.bottom_screen.scissor.get_mp(8)))\
                        in [Colour.MP_GREEN, Colour.MP_RED]:
                    if self.opponent.number_of_moves()[0] == 3:
                        my_MP = [0, 0, 0]
                        for i in range(10):
                            point = self.bottom_screen.rock.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[0] = i + 1
                            point = self.bottom_screen.paper.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[1] = i + 1
                            point = self.bottom_screen.scissor.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[2] = i + 1
                    else:
                        my_MP = [0, 0, 0, 0]
                        for i in range(10):
                            point = self.bottom_screen.rock.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[0] = i + 1
                            point = self.bottom_screen.paper.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[1] = i + 1
                            point = self.bottom_screen.scissor.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) == Colour.MP_RED:
                                my_MP[2] = i + 1
                            point = self.bottom_screen.fourth.get_mp(i)
                            if get_mp_colour_fuzzy(surrounding_pixels(frame, point)) in [Colour.MP_RED, Colour.NONE]\
                                    and i not in [0, 9]: # these points are covered by the move name box
                                my_MP[3] = i + 1

                    self.turn.my_mp_levels = my_MP
                    # set to how many sections are red (used)

                    # run the classifier again, if the result changes, update the UI
                    if self.classifier:
                        self.prediction = self.classifier.predict_proba([self.turn.to_csv(self.opponent.number_of_moves())[:-1]])

                    self.turn_state = 7
            case 7:
                # find out which moves were used
                my_attack_pos = self.top_screen.my_attack.get_move_type(3)
                my_attack_col = get_move_colour_fuzzy(surrounding_pixels(frame, my_attack_pos))
                their_attack_pos = self.top_screen.their_attack.get_move_type(3)
                their_attack_col = get_move_colour_fuzzy(surrounding_pixels(frame, their_attack_pos))

                if my_attack_col != Colour.NONE and their_attack_col != Colour.NONE:
                    # save move choices to turn, create new turn
                    match my_attack_col:
                        case Colour.RED:
                            self.turn.my_move = 1
                        case Colour.BLUE:
                            self.turn.my_move = 2
                        case Colour.YELLOW:
                            self.turn.my_move = 3

                    match their_attack_col:
                        case Colour.RED:
                            self.turn.their_move = 1
                        case Colour.BLUE:
                            self.turn.their_move = 2
                        case Colour.YELLOW:
                            self.turn.their_move = 3

                    # save turn if needed
                    if cfg.save and self.opponent:
                        with open(self.opponent.get_turn_file(), "a", newline='') as file:
                            write_result = csv.writer(file).writerow(self.turn.to_csv(self.opponent.number_of_moves()))
                    # create new turn with last move
                    self.turn = new_turn(self.turn)
                    # repeat
                    self.turn_state = 1


class Prediction:
    """
    Converts list of probabilities into an actionable suggestion.
    Uses 0 - Rock, 1 - Paper, 2 - Scissor
    """
    def __init__(self, probabilities):
        self.paper_win = self.rock_tie = probabilities[0]
        self.scissor_win = self.paper_tie = probabilities[1]
        self.rock_win = self.scissor_tie = probabilities[2]

        # try to find a better way of prioritizing wins but trying to get the win/tie option when available
        self.rock_prob = 2 * self.rock_win + self.rock_tie
        self.paper_prob = 2 * self.paper_win + self.paper_tie
        self.scissor_prob = 2 * self.scissor_win + self.scissor_tie

    def best_move(self):
        if self.rock_prob > self.paper_prob and self.rock_prob > self.scissor_prob:
            return 0, "rock", self.rock_win, self.rock_tie
        if self.paper_prob > self.rock_prob and self.paper_prob > self.scissor_prob:
            return 1, "paper", self.paper_win, self.paper_tie
        # if self.scissor_prob > self.rock_prob and self.scissor_prob > self.paper_prob:
        else:
            return 2, "scissor", self.scissor_win, self.scissor_tie
