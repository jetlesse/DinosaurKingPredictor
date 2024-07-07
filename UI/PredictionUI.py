import wx
import wxasync
from wx.lib.statbmp import GenStaticBitmap
from engine import Engine, Prediction
from Config import config


class PredictionUI(wx.Frame):

    def __init__(self, parent):
        super(PredictionUI, self).__init__(parent, title="Move Prediction")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.top_screen_cfgs = config.read_yaml_config("Config/Screens_Live/top_screen_config.yaml")
        self.bottom_screen_cfgs = config.read_yaml_config("Config/Screens_Live/bottom_screen_config.yaml")

        self.fight = None
        self.prediction_engine = None

        self.blank_icon = wx.Bitmap("UI/Resources/BlankIcon.png", wx.BITMAP_TYPE_PNG)
        self.icons = [
            wx.Bitmap("UI/Resources/RockIcon.png", wx.BITMAP_TYPE_PNG),
            wx.Bitmap("UI/Resources/PaperIcon.png", wx.BITMAP_TYPE_PNG),
            wx.Bitmap("UI/Resources/ScissorIcon.png", wx.BITMAP_TYPE_PNG)
        ]

        self.fight_text = wx.StaticText(panel, label="Current fight: ")
        sizer.Add(self.fight_text, 0, wx.ALL | wx.LEFT, 3)
        prediction_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(prediction_sizer)
        self.move_image = GenStaticBitmap(panel, -1, self.blank_icon, size=wx.Size(100, 100))
        prediction_sizer.Add(self.move_image, 0, wx.ALL | wx.LEFT, 3)
        probability_sizer = wx.BoxSizer(wx.VERTICAL)
        prediction_sizer.Add(probability_sizer)
        self.predict_text = wx.StaticText(panel, label="predicting: \n")
        probability_sizer.Add(self.predict_text, 0, wx.ALL | wx.LEFT, 3)
        self.prob_text = wx.StaticText(panel, label="win: \ntie: ")
        probability_sizer.Add(self.prob_text, 0, wx.ALL | wx.LEFT, 3)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_update, self.timer)
        self.timer.Start(16) # ~60 fps

        panel.SetSizer(sizer)

    def change_fight(self, fight, cfg):
        """
        stop and remove existing prediction engine, otherwise it will continue running in the background, orphaned.
        create a new prediction engine and run it with the configs for the new fight running in a window
        :param fight: config for the battle to analyze
        :param cfg: a GeneralConfig object. Properties can be used to set or optimize execution
        :return: None
        """
        self.fight = fight
        self.fight_text.SetLabel("Current fight: " + self.fight.display_name)
        if self.prediction_engine is not None:
            self.prediction_engine.stop = True
        self.prediction_engine = None
        # if the id is low enough then use 3, otherwise use 4
        if fight.number_of_moves()[1] == 3:
            top_screen = self.top_screen_cfgs[0].get_screen()
        else:
            top_screen = self.top_screen_cfgs[1].get_screen()

        if fight.number_of_moves()[0] == 3:
            bottom_screen = self.bottom_screen_cfgs[0].get_screen()
        else:
            bottom_screen = self.bottom_screen_cfgs[1].get_screen()

        self.prediction_engine = Engine(top_screen, bottom_screen)

        self.Show()
        # run in another thread so UI is not blocked by engine
        wxasync.StartCoroutine(self.prediction_engine.run_window(fight, cfg), self)

    def timer_update(self, event):
        if self.prediction_engine is not None:
            prediction = self.prediction_engine.prediction
            if prediction is None:
                self.set_blank_prediction()
            else:
                if len(prediction) == 1:
                    prediction = prediction[0]
                best_move = Prediction(prediction).best_move()
                self.predict_text.SetLabel("predicting: {0}\n{1}".format(best_move[1], prediction))
                self.prob_text.SetLabel("win: {0:>5.2f}\ntie: {1:>5.2f}".format(best_move[2], best_move[3]))
                self.move_image.SetBitmap(self.icons[best_move[0]])

    def set_blank_prediction(self):
        self.predict_text.SetLabel("predicting: \n")
        self.move_image.SetBitmap(self.blank_icon)
        self.prob_text.SetLabel("win: \ntie: ")

    def on_close(self, event):
        if event.CanVeto():
            if self.prediction_engine is not None:
                self.prediction_engine.stop = True
            self.prediction_engine = None
            event.Veto()
            self.set_blank_prediction()
            self.Refresh()
            self.Update()
            # frame doesn't update to "blank" if it is hidden immediately
            wx.CallLater(1, self.Hide)
        else:
            if self.prediction_engine is not None:
                self.prediction_engine.stop = True
            # it keeps running for some reason
            self.prediction_engine = None
            self.set_blank_prediction()
            self.Destroy()
