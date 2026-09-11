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
    pruned_branches = 0  # Contador de ramas podadas

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        AlphaBeta.pruned_branches = 0
        moves = current_state.available_moves()
        best_move = None
        
        alpha = None
        beta = None
        best_value = None

        for move in moves:
            next_state = current_state.next_state(move)
            value = AlphaBeta.alphabeta(next_state, depth=1, alpha=alpha, beta=beta)

            if objective.value == 0:  # MAX
                if best_value is None or value > best_value:
                    best_value = value
                    best_move = move
                # Actualizar alpha usando None
                if alpha is None or best_value > alpha:
                    alpha = best_value
            else:  # MIN
                if best_value is None or value < best_value:
                    best_value = value
                    best_move = move
                # Actualizar beta usando None
                if beta is None or best_value < beta:
                    beta = best_value

        print(f"Pruned branches: {AlphaBeta.pruned_branches}")
        return best_move

    @staticmethod
    def alphabeta(state: State, depth: int, alpha: float, beta: float):
        MAX_DEPTH = 8
        moves = state.available_moves()

        if depth >= MAX_DEPTH or not moves:
            return state.score

        best_value = None

        if state.current_player == 0:  # MAX
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)

                # Asignación y actualización sin usar max()
                if best_value is None or value > best_value:
                    best_value = value
                if alpha is None or best_value > alpha:
                    alpha = best_value

                # Condición de poda considerando que beta puede ser None
                if beta is not None and alpha is not None and alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return best_value

        else:  # MIN
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)

                # Asignación y actualización sin usar min()
                if best_value is None or value < best_value:
                    best_value = value
                if beta is None or best_value < beta:
                    beta = best_value

                # Condición de poda considerando que alpha puede ser None
                if alpha is not None and beta is not None and alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return best_value