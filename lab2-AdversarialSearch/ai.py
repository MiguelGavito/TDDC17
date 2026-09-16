import random

from game import AI, State, Objective


MAX_DEPTH = 8


def _pick_move(utilities, objective: Objective):
    if not utilities:
        return None

    if objective is Objective.MAX:
        target_value = max(utilities.values())
    else:
        target_value = min(utilities.values())

    # Deterministic tie-break keeps behavior reproducible.
    return min(pit for pit, value in utilities.items() if value == target_value)


class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()

        available_moves = state.available_moves()
        if not available_moves:
            return None

        return random.choice(available_moves)


class MinMax(AI):
    expanded_nodes = 0  # adding expanded nodes counter variable
    
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        MinMax.expanded_nodes = 0  #added
        utilities = {}

        for move in current_state.available_moves():
            next_state = current_state.next_state(move)
            utilities[move] = MinMax.minmax(next_state, depth=1)

        print(f"Expanded nodes: {MinMax.expanded_nodes}")
        return _pick_move(utilities, objective)

    @staticmethod
    def minmax(state: State, depth: int = 0):
        MinMax.expanded_nodes += 1 #adding  1 to expanded nodes counter
        moves = state.available_moves()
    
        
        if depth >= MAX_DEPTH or not moves:
            return state.score

        best_value = None
        for move in moves:
            next_state = state.next_state(move)
            value = MinMax.minmax(next_state, depth + 1)
                
            if state.current_player == 0: # MAX
                if best_value is None or value > best_value:
                    best_value = value

            else: #MIN
                if best_value is None or value < best_value:
                    best_value = value

        return best_value


class AlphaBeta(AI):
    pruned_branches = 0  # counter for pruned branches
    expanded_nodes = 0  # counter for expanded nodes

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        AlphaBeta.pruned_branches = 0
        AlphaBeta.expanded_nodes = 0
        alpha = float('-inf')  #worst case for MAX
        beta = float('inf') #worst case for MIN
        utilities = {}
        
        for move in current_state.available_moves():
            next_state = current_state.next_state(move)
            value = AlphaBeta.alphabeta(next_state, depth=1, alpha=alpha, beta=beta)
            utilities[move] = value

            if objective is Objective.MAX:  # MAX
                alpha = max(alpha, value)
            else:  # MIN
                beta = min(beta, value)
        

        print(f"Pruned branches: {AlphaBeta.pruned_branches}")
        print(f"Expanded nodes: {AlphaBeta.expanded_nodes}")
        return _pick_move(utilities, objective)

    @staticmethod
    def alphabeta(state: State, depth: int, alpha: float, beta: float):
        AlphaBeta.expanded_nodes += 1  # Increment the expanded nodes counter
        moves = state.available_moves()

        if depth >= MAX_DEPTH or not moves:
            return state.score

        best_value = None
        
        if state.current_player == 0:  # MAX
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)

                # set and update 
                if best_value is None or value > best_value:
                    best_value = value
                if best_value > alpha:
                    alpha = best_value

                # check for pruning condition 
                if  alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return best_value

        else:  # MIN
            for move in moves:
                next_state = state.next_state(move)
                value = AlphaBeta.alphabeta(next_state, depth + 1, alpha, beta)

                # set and update 
                if best_value is None or value < best_value:
                    best_value = value
                if best_value < beta:
                    beta = best_value

                # check for pruning condition considering that alpha can be None
                if alpha >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
                
            return best_value