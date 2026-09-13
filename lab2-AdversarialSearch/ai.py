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
    expanded_nodes = 0  # adding expanded nodes counter variable
    
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        MinMax.expanded_nodes = 0  #added
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

        print(f"Expanded nodes: {MinMax.expanded_nodes}")
        return best_move

    @staticmethod
    def minmax(state: State, depth: int = 0):
        MinMax.expanded_nodes += 1 #adding  1 to expanded nodes counter
        MAX_DEPTH = 8 #required depth
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
        moves = current_state.available_moves()
        best_move = None
        
        alpha = float('-inf')  #worst case for MAX
        beta = float('inf') #worst case for MIN
        best_value = None
        
        for move in moves:
            next_state = current_state.next_state(move)
            value = AlphaBeta.alphabeta(next_state, depth=1, alpha=alpha, beta=beta)

            if objective.value == 0:  # MAX
                if best_value is None or value > best_value:
                    best_value = value
                    best_move = move
                # Actualizar alpha usando None
                if best_value > alpha:
                    alpha = best_value
            else:  # MIN
                if best_value is None or value < best_value:
                    best_value = value
                    best_move = move
                # Actualizar beta usando None
                if best_value < beta:
                    beta = best_value
        

        print(f"Pruned branches: {AlphaBeta.pruned_branches}")
        print(f"Expanded nodes: {AlphaBeta.expanded_nodes}")
        return best_move

    @staticmethod
    def alphabeta(state: State, depth: int, alpha: float, beta: float):
        AlphaBeta.expanded_nodes += 1  # Increment the expanded nodes counter
        MAX_DEPTH = 8
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