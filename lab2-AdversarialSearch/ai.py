import random

from game import AI, State, Objective


class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()

        available_moves = state.available_moves()
        if not available_moves:
            return None

        return random.choice(available_moves)


class MinMax(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):

        # check my options
        moves = current_state.available_moves()

        best_move = None
        best_value = None

        for move in moves:
            next_state = current_state.next_state(move)
            value = MinMax.minmax(next_state)

        if best_value is None:
            best_value = value
            best_move = move

        elif objective.value == 0: # MAX
            if value > best_value:
                best_value = value
                best_move = move
        else: # MIN
            if value < best_value:
                best_value = value
                best_move = move

        
        return best_move

    @staticmethod
    def minmax(state: State):
        moves = state.available_moves()

        
        if not moves:
            return 0

        best_value = None
        
        for move in moves:
            next_state = state.next_state(move)
            value = MinMax.minmax(next_state)
                
            if state.current_player == 0: # MAX
                if best_value is None or value > best_value:
                    best_value = value

            else: #MIN
                if best_value is None or value < best_value:
                    best_value = value

        return best_value


class AlphaBeta(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        pass
