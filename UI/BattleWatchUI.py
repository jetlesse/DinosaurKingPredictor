import copy

import wx

import Config.config
import capture
from Config import config
from GameData import fights
from engine import Engine


class BattleWatchUI(wx.Frame):
    def __init__(self, parent, cfg):
        super(BattleWatchUI, self).__init__(parent, title="Reading battle video")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.top_screen_cfgs = config.read_yaml_config("Config/Screens_Recording/top_screen_config.yaml")
        self.bottom_screen_cfgs = config.read_yaml_config("Config/Screens_Recording/bottom_screen_config.yaml")
        self.prediction_engine = None

        # don't set save to True for main config object, only for this instance
        self.cfg = copy.deepcopy(cfg)
        self.cfg.save = True
        battles = Config.config.read_yaml_config("Config/battle_times.yaml")

        self.status_text = wx.StaticText(panel)
        sizer.Add(self.status_text, 0, wx.ALL | wx.LEFT, 3)

        self.Show()

        for idx, battle in enumerate(battles):
            opponent = next((x for x in fights.fights if x.id == str(battle.id)), None)
            if opponent.number_of_moves() == 3:
                self.prediction_engine = Engine(self.top_screen_cfgs[0].get_screen(),
                                                self.bottom_screen_cfgs[0].get_screen())
            else:
                self.prediction_engine = Engine(self.top_screen_cfgs[1].get_screen(),
                                                self.bottom_screen_cfgs[1].get_screen())

            self.status_text.SetLabel("Reading data for battle " + str(idx) + " against " + opponent.display_name)
            self.prediction_engine.run_video(battle, self.cfg)

        self.status_text.SetLabel("Complete. Read " + str(len(battles)) + " battles.")
