import wx
from setup import Setup


class SetupUI(wx.Frame):
    def __init__(self, parent, setup: Setup):
        super(SetupUI, self).__init__(parent, title="Test config setup")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.setup = setup
        state_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prev_button = wx.Button(panel, label="<<")
        self.prev_button.Bind(wx.EVT_BUTTON, self.previous)
        self.state_label = wx.StaticText(panel, label="State: 0")
        self.next_button = wx.Button(panel, label=">>")
        self.next_button.Bind(wx.EVT_BUTTON, self.next)
        state_sizer.Add(self.prev_button, 1, wx.ALL | wx.LEFT, 3)
        state_sizer.Add(self.state_label, 1, wx.ALL | wx.CENTER, 3)
        state_sizer.Add(self.next_button, 1, wx.ALL | wx.RIGHT, 3)
        sizer.Add(state_sizer)
        self.print_button = wx.Button(panel, label="print debug output")
        self.print_button.Bind(wx.EVT_BUTTON, self.print)
        sizer.Add(self.print_button)

        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.stop_button = wx.Button(panel, label="Stop")
        self.stop_button.Bind(wx.EVT_BUTTON, self.stop)
        control_sizer.Add(self.stop_button, 1, wx.ALL, 3)
        self.Bind(wx.EVT_CLOSE, self.stop)

        self.pause_button = wx.Button(panel, label="Pause")
        self.pause_button.Bind(wx.EVT_BUTTON, self.pause)
        control_sizer.Add(self.pause_button, 1, wx.ALL, 3)
        sizer.Add(control_sizer)

        panel.SetSizer(sizer)
        self.Show()
        self.setup.run()

    def previous(self, event):
        self.setup.change_state(self.setup.state - 1)
        self.state_label.SetLabel("State: " + str(self.setup.state))

    def next(self, event):
        self.setup.change_state(self.setup.state + 1)
        self.state_label.SetLabel("State: " + str(self.setup.state))

    def print(self, event):
        self.setup.print_output = True

    def stop(self, event):
        self.setup.stop = True
        self.Destroy()

    def pause(self, event):
        if self.setup.pause:
            self.pause_button.SetLabel("Resume")
        else:
            self.pause_button.SetLabel("Pause")
        self.setup.pause = not self.setup.pause
