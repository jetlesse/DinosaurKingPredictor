# represents the information we can have about a turn
# including the moves from last turn, current MP levels, what the opponent said
def new_turn(last_turn):
    turn = Turn()
    turn.base_turn(last_turn.my_move, last_turn.their_move, last_turn.my_dino, last_turn.their_dino)
    return turn


class Turn:
    def __init__(self):
        self.saying = 0
        self.their_move = 0
        self.my_move = 0
        self.their_dino = 0
        self.my_dino = 0
        self.their_mp_levels = [0,0,0]
        self.my_mp_levels = [0,0,0]
        self.their_last_move = 0
        self.my_last_move = 0

    def empty_turn(self):
        self.my_last_move = 0

    def base_turn(self, my_last_move, their_last_move, my_dino, their_dino):
        self.my_last_move = my_last_move
        self.their_last_move = their_last_move
        self.my_dino = my_dino
        self.their_dino = their_dino

    def full_turn(self, saying, my_last_move, their_last_move,
                  my_mp_levels, their_mp_levels, my_dino, their_dino, my_move, their_move):
        self.saying = saying
        self.my_last_move = my_last_move
        self.their_last_move = their_last_move
        self.my_mp_levels = my_mp_levels
        self.their_mp_levels = their_mp_levels
        self.my_dino = my_dino
        self.their_dino = their_dino
        self.my_move = my_move
        self.their_move = their_move

    def to_csv(self, number_of_moves):
        output = [self.saying, self.my_last_move, self.their_last_move,
                    self.my_mp_levels[0], self.my_mp_levels[1], self.my_mp_levels[2]]
        if number_of_moves[0] == 4:
            output.append(self.my_mp_levels[3])

        output.append(self.their_mp_levels[0])
        output.append(self.their_mp_levels[1])
        output.append(self.their_mp_levels[2])
        if number_of_moves[1] == 4:
            output.append(self.their_mp_levels[3])

        output.append(self.my_dino)
        output.append(self.their_dino)
        output.append(self.their_move)
        return output
