import wx

import setup
import solver
from Config import config
from UI.BattleWatchUI import BattleWatchUI
from UI.PredictionUI import PredictionUI
from UI.SetupUI import SetupUI


class UIMain(wx.Frame):

    def __init__(self, parent, fight_order, cfg):
        super(UIMain, self).__init__(parent, title="Dinosaur King Prediction App")
        panel = wx.Panel(self)
        self.fight_idx = -1
        self.fight_order = fight_order
        self.cfg = cfg
        self.prediction_screen = None
        self.setup_screen = None

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_options_sizer = wx.BoxSizer(wx.VERTICAL)
        extra_options_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(main_options_sizer, 0)
        sizer.Add(extra_options_sizer, 0)

        # read video file for turns
        self.read_button = wx.Button(panel, label="Add data from video")
        extra_options_sizer.Add(self.read_button, 0, wx.ALL | wx.CENTER, 3)
        self.read_button.Bind(wx.EVT_BUTTON, self.read_video)

        # Train model
        self.train_button = wx.Button(panel, label="Train")
        extra_options_sizer.Add(self.train_button, 0, wx.ALL | wx.CENTER, 3)
        self.train_button.Bind(wx.EVT_BUTTON, self.train_model)

        # Train all models
        self.train_all_button = wx.Button(panel, label="Train all fights")
        extra_options_sizer.Add(self.train_all_button, 0, wx.ALL | wx.CENTER, 3)
        self.train_all_button.Bind(wx.EVT_BUTTON, self.train_all_models)

        # Test setup
        self.setup_button3 = wx.Button(panel, label="Test screen config\n3 moves")
        extra_options_sizer.Add(self.setup_button3, 0, wx.ALL | wx.CENTER, 3)
        self.setup_button3.Bind(wx.EVT_BUTTON, self.test_setup_3)

        self.setup_button4 = wx.Button(panel, label="Test screen config\n4 moves")
        extra_options_sizer.Add(self.setup_button4, 0, wx.ALL | wx.CENTER, 3)
        self.setup_button4.Bind(wx.EVT_BUTTON, self.test_setup_4)

        # Window or Video
        self.window_select = wx.RadioButton(panel, label="Window/Live", style=wx.RB_GROUP)
        self.video_select = wx.RadioButton(panel, label="Video")
        extra_options_sizer.Add(self.window_select, 0, wx.ALL | wx.CENTER, 3)
        extra_options_sizer.Add(self.video_select, 0, wx.ALL | wx.CENTER, 3)

        # select fight
        data = [fight.display_name for fight in fight_order if fight.id != '0000']
        self.predict_choice = wx.Choice(panel, choices=data, )
        main_options_sizer.Add(self.predict_choice, 0, wx.ALL | wx.CENTER, 3)
        self.predict_choice.Bind(wx.EVT_CHOICE, self.get_choice)

        # open prediction screen
        self.predict_button = wx.Button(panel, label="Predict")
        self.predict_button.Bind(wx.EVT_BUTTON, self.start_button)
        main_options_sizer.Add(self.predict_button, 0, wx.ALL | wx.CENTER, 3)
        # self.predict_label = wx.StaticText(panel, label="chosen: ")
        # sizer.Add(self.predict_label, 0, wx.ALL | wx.LEFT, 3)

        next_prev_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_options_sizer.Add(next_prev_sizer)
        # select next/previous fight
        self.prev_button = wx.Button(panel, label="Previous")
        self.prev_button.Bind(wx.EVT_BUTTON, self.previous)
        self.next_button = wx.Button(panel, label="Next")
        self.next_button.Bind(wx.EVT_BUTTON, self.next)
        next_prev_sizer.Add(self.prev_button, 1, wx.ALL | wx.LEFT, 3)
        next_prev_sizer.Add(self.next_button, 1, wx.ALL | wx.RIGHT, 3)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        panel.SetSizer(sizer)
        self.Show()

    def get_choice(self, event):
        self.fight_idx = self.predict_choice.GetSelection()

    def start_button(self, event):
        self.fight_idx = self.predict_choice.GetSelection()
        self.start_prediction()

    def previous(self, event):
        if self.fight_idx > 0:
            self.fight_idx -= 1
            self.predict_choice.SetSelection(self.fight_idx)
            self.start_prediction()

    def next(self, event):
        if self.fight_idx < self.predict_choice.GetCount() - 1:
            self.fight_idx += 1
            self.predict_choice.SetSelection(self.fight_idx)
            self.start_prediction()

    def start_prediction(self):
        # run the prediction engine with the current id
        fight = self.fight_order[self.fight_idx + 1]
        if self.prediction_screen is None:
            self.prediction_screen = PredictionUI(self)
        self.prediction_screen.change_fight(fight=fight, cfg=self.cfg)

    def train_model(self, event):
        fight = self.fight_order[self.fight_idx + 1]
        clf = solver.train_model(fight.get_turn_file())
        fight.save_classifier(clf)

    def train_all_models(self, event):
        for fight in self.fight_order[1:]:
            clf = solver.train_model(fight.get_turn_file())
            fight.save_classifier(clf)

    def read_video(self, event):
        battle_watch = BattleWatchUI(self, cfg=self.cfg)

    def test_setup_3(self, event):
        # first object is for 3 moves
        input_type = "Live"
        if self.window_select.GetValue():
            top_screen = config.read_yaml_config("Config/Screens_Live/top_screen_config.yaml")[0].get_screen()
            bottom_screen = config.read_yaml_config("Config/Screens_Live/bottom_screen_config.yaml")[0].get_screen()
        else:
            top_screen = config.read_yaml_config("Config/Screens_Recording/top_screen_config.yaml")[0].get_screen()
            bottom_screen = config.read_yaml_config("Config/Screens_Recording/bottom_screen_config.yaml")[0].get_screen()
            input_type = "Recording"

        s = setup.Setup(top_screen, bottom_screen, self.cfg, input_type)
        self.setup_screen = SetupUI(self, s)

    def test_setup_4(self, event):
        # second object is for 4 moves
        input_type = "Live"
        if self.window_select.GetValue():
            top_screen = config.read_yaml_config("Config/Screens_Live/top_screen_config.yaml")[1].get_screen()
            bottom_screen = config.read_yaml_config("Config/Screens_Live/bottom_screen_config.yaml")[1].get_screen()
        else:
            top_screen = config.read_yaml_config("Config/Screens_Recording/top_screen_config.yaml")[1].get_screen()
            bottom_screen = config.read_yaml_config("Config/Screens_Recording/bottom_screen_config.yaml")[1].get_screen()
            input_type = "Recording"

        s = setup.Setup(top_screen, bottom_screen, self.cfg, input_type)
        self.setup_screen = SetupUI(self, s)

    def on_close(self, event):
        if self.prediction_screen is not None:
            self.prediction_screen.Close()
        self.Destroy()
