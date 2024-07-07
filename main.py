import wxasync
import asyncio

from Config import config
from UI.UIMain import UIMain
from GameData import fights


async def main():
    app = wxasync.WxAsyncApp()
    gui = UIMain(None, fight_order=fights.fight_order, cfg=cfg)
    app.SetTopWindow(gui)
    await app.MainLoop()
    exit(0)

if __name__ == '__main__':

    cfg = config.read_yaml_config("Config/general_config.yaml")[0]
    top_screen_cfgs = config.read_yaml_config("Config/Screens_Live/top_screen_config.yaml")
    bottom_screen_cfgs = config.read_yaml_config("Config/Screens_Live/bottom_screen_config.yaml")
    top_screen = top_screen_cfgs[0].get_screen()
    bottom_screen = bottom_screen_cfgs[0].get_screen()

    fights.read_fight_data()
    asyncio.run(main())
