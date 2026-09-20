import random
from game import AI, State, Objective


class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        available_moves = current_state.available_moves()
        if not available_moves:
            return None
        return random.choice(available_moves)


class MinMax(AI):
    expanded_nodes = 0

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        MinMax.expanded_nodes = 0
        moves = current_state.available_moves()

        if not moves:
            return None

        best_move = None
        # Objective.MAX corresponds to value 1 in the Objective Enum
        is_max = (objective == Objective.MAX)
        best_value = float('-inf') if is_max else float('inf')

        for move in moves:
            next_state = current_state.next_state(move)
            # Start recursion at depth 1
            value = MinMax.minmax(next_state, depth=1)

            if is_max:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        print(f"Expanded nodes: {MinMax.expanded_nodes}")
        return best_move

    @staticmethod
    def minmax(state: State, depth: int):
        MinMax.expanded_nodes += 1
        MAX_DEPTH = 8
        moves = state.available_moves()

        # Terminal state condition or depth limit reached
        if depth >= MAX_DEPTH or not moves:
            return state.score

        # Player 0 acts as MAX (positive score favors Player 0)
        if state.current_player == 0:
            best_value = float('-inf')
            for move in moves:
                next_state = state.next_state(move)
                value = MinMax.minmax(next_state, depth + 1)
                best_value = max(best_value, value)
            return best_value

        # Player 1 acts as MIN (negative score favors Player 1)
        else:
            best_value = float('inf')
            for move in moves:
                next_state = state.next_state(move)
                value = MinMax.minmax(next_state, depth + 1)
                best_value = min(best_value, value)
            return best_value


class AlphaBeta(AI):
    pruned_branches = 0
    expanded_nodes = 0

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        AlphaBeta.pruned_branches = 0
        AlphaBeta.expanded_nodes = 0
        moves = current_state.available_moves()

        if not moves:
            return None

        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        # Objective.MAX corresponds to value 1 in the Objective Enum
        is_max = (objective == Objective.MAX)
        best_value = float('-inf') if is_max else float('inf')

        for move in moves:
            next_state = current_state.next_state(move)
            value = AlphaBeta.alphabeta(next_state, depth=1, alpha=alpha, beta=beta)

            if is_max:
                if value > best_value:
                    best_value = value
                    best_move = move
                # Update alpha bound for root evaluation
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                # Update beta bound for root evaluation
                beta = min(beta, best_value)

        print(f"Pruned branches: {AlphaBeta.pruned_branches}")
        print(f"Expanded nodes: {AlphaBeta.expanded_nodes}")
        return best_move

    @staticmethod
    def alphabeta(state: State, depth: int, alpha: float, beta: float):
        AlphaBeta.expanded_nodes += 1
        MAX_DEPTH = 8
        moves = state.available_moves()

        # Terminal state condition or depth limit reached
        if depth >= MAX_DEPTH or not moves:
            return state.score

        # Player 0 acts as MAX (positive score favors Player 0)
        if state.current_player == 0:
            best_value = float('-inf')
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)

                # Alpha-Beta Pruning
                if alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return best_value

        # Player 1 acts as MIN (negative score favors Player 1)
        else:
            best_value = float('inf')
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)

                # Alpha-Beta Pruning
                if alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return best_value