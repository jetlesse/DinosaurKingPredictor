Dinosaur King (DS) Move Predictor App
This is an application which is used to watch the gameplay from the Nintendo DS Dinosaur King game (English). This will learn from previously seen turns and predict what the AI will be using next.

This app can watch the game using either a video file for training or from a window showing both screens of the DS. The app currently only supports real time game play on Windows.

Requirements:
- Python 3.10+ (other versions have not been tested)
- [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

Required Packages:
- pywin32
- Pillow
- pytesseract
- PyYAML
- opencv-python
- wxPython
- wxasync
- asyncio
- scikit-learn
- numpy

Run the application using `py main.py`

Recorded Gameplay

Add entries to the battle_times.yaml file. This requires the fight ID from fight.csv for the opponent, then the start time and end time in the form HH:mm:ss. You can list multiple battles in this file like this.

    - !Battle
      id: 01001
      start_time: 00:00:05
      end_time: 00:01:21
    - !Battle
      id: 01001
      start_time: 00:01:48
      end_time: 00:02:59

Configs

General Config

- my_dino: If you are using only one dinosaur, or only dinosaurs with the same critical type, such as the speedrun route you can lock the dinosaur you are using to save time reading the dinosaur name every turn.
- show_screen: True or False. Whether to show the screen that the app is seeing, for debugging purposes.
- fps: If using a video file, set the fps of the recording, so the app can accurately find where in the video the timestamps are.
- save: True or False. Whether to save the turn data into files or only run the predictions.
- window_name: The whole or part of the window title. The app will look for a window with this in the title. If there are multiple possible matches, the window that is found is not guaranteed, try to be as specific as possible for the window you are targeting.
- filename: The path to a recorded video file to be read in for recorded gameplay.
- start_time: The timestamp in the recording to start from for checking setup.

Screen configs

Set the pixel coordinates of the special elements of the top and bottom screens. Try using the basic screen config files, which chooses locations based on proportions of the total screen area. If this does not correctly locate all the elements on the screen then you will need to use the top_screen_config.yaml and bottom_screen_config.yaml files and input the correct values there. Location testing can be used to display where the app will be looking for the screen elements to easily values for the correct locations.

The train feature will only read from video files, the prediction feature will only watch from a window in real time. Both will be able to save turn data.

Game Data

The paths are all stored by the continent, then the name of the location in which the fight takes place (e.g. Europe/South for the southern area of Europe). Most enemies are named robot_# with the number increasing in the order that they can be encountered.
The grid of fights in the final dungeon is ordered as such:

|        |    | Seth |     |        |
|--------|----|------|-----|--------|
| 1      |    |      |     | 5      |
| Ursula | 3  |      | Rod | Zander |
| 2      | Ed |      | 4   | 6      |

Sayings

The text that enemies say before their turns, each line is a separate saying in no particular order. One of the lines must be blank to represent the enemy not saying anything. All text should be only lowercase letters, spaces and the following punctuation `.!?,-`. Apostrophes are ignored so reading the text is faster and more accurate.

Dinos

The names of the dinosaurs that are used by each enemy. Each dinosaur is listed on a separate line.

Turn Data

CSV files representing a collection of all turns recorded by the app for each enemy. These files have the following columns:

- saying: A number representing the line in the Sayings file for this enemy which matches what was said.
- my/their last move: The move used in the last turn. 1 = Rock, 2 = Paper, 3 = Scissors.
- my rock/paper/scissors/fourth: The number of MP bars used up (red) at the beginning of the turn for each of the player's moves.
- their rock/paper/scissors/fourth: The number of MP bars used up (red) at the beginning of the turn for each of the enemy's moves.
- my/their dino: A number representing the line in the dinos file for the player/enemy which matches the current dinosaur's name.

This is the data which is used to train the AI models.

Models

The saved versions of the AI models for each enemy. These are read in as needed to avoid having to retrain on every execution. The model must be trained prior to attempting to predict the fight.