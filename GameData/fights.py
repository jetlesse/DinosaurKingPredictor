import csv
from os import path

import solver

fights = []
fight_order = []


def read_fight_data():
    with open(path.join(path.dirname(__file__), "fights.csv"), "r", newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        global fights
        fights = [Fight(id, continent, location, name, display_name)
                  for id, continent, location, name, display_name in csv_reader]

    with open(path.join(path.dirname(__file__), "fightOrder.csv"), "r", newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        order = [id[0] for id in csv_reader]

        global fight_order
        fight_order = [next((f for f in fights if f.id == x), None) for x in order]


class FightData:
    def __init__(self):
        print(path.dirname(__file__))
        print(path.join(path.dirname(__file__), "fights.csv"))
        with open(path.join(path.dirname(__file__), "fights.csv"), "r", newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)

            global fights
            fights = [Fight(id, continent, location, name, display_name)
                      for id, continent, location, name, display_name in csv_reader]


class Fight:
    def __init__(self, id, continent, location, name, display_name):
        self.id = id
        self.continent = continent
        self.location = location
        self.name = name
        self.display_name = display_name
        self.dinos = []
        self.sayings = []

    def get_turn_file(self):
        return path.join(path.dirname(__file__), "TurnData", self.continent, self.location, self.name + ".csv")

    def load_classifier(self):
        return solver.read_model(path.join(path.dirname(__file__),
                                           "Models", self.continent, self.location, self.name + ".pkl"))

    def save_classifier(self, clf):
        solver.write_model(clf, path.join(path.dirname(__file__),
                                          "Models", self.continent, self.location, self.name + ".pkl"))

    def read_dino_file(self):
        filepath = path.join(path.dirname(__file__), "StringConversion", "Dinos",
                             self.continent, self.location, self.name + ".txt")
        with open(filepath) as file:
            self.dinos = [line.replace("\n", "") for line in file.readlines()]

    def read_saying_file(self):
        filepath = path.join(path.dirname(__file__), "StringConversion", "Sayings",
                             self.continent, self.location, self.name + ".txt")
        with open(filepath) as file:
            self.sayings = [line.replace("\n", "") for line in file.readlines()]

    def read_all_files(self):
        self.read_dino_file()
        self.read_saying_file()

    def number_of_moves(self):
        """
        The fight id number is in the 2000s for Europe and Asia of the main game.
        All other areas (3000+) and returns to those areas (11000+, not tested) have 4 moves.
        :return: tuple (x,y). The number of moves the user and the opponent have in the fight
        """
        my_moves = 4
        if int(self.id) // 10 ** 3 < 3:
            my_moves = 3
        their_moves = my_moves
        if int(self.id) == 3303:
            # Exception for first Ursula fight
            their_moves = 3
        return (my_moves, their_moves)