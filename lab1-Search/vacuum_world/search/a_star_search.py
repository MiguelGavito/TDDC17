from typing import List, Optional
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch
import heapq

class AStarNode(SearchNode):    
    # TODO: Implement this class
    """Represents a node in the search tree of a star"""

    def __init__(self, state: GridPos, parent: Optional['SearchNode'] = None, action: Optional[str] = None, cost: float = 0.0, heuristic: float = 0.0):
        """Initialize a search node.
        
        Args:
            state: The state (grid position) this node represents
            parent: The parent node (None for root)
            action: The action taken to reach this state (unused, kept for compatibility)
            cost: The path cost to reach this state
        """
        super().__init__(state, parent, cost)
        self.heuristic = heuristic

    def get_heuristic(self) -> float:
        """Get the heuristic (float) of this node.
        
        Returns:
            The distance to the goal
        """
        return self.heuristic

class AStarSearch(BaseSearch):

    def __init__(self):
        """
        Initialize the search algorithm similar to bfs
        """
        super().__init__()

        self.path: List[SearchNode] = []

        # Tailor the following data structures to the needs of the search algorithm
        self.frontier = []
        self.explored = []
        self.counter = 0
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perform a breath first search to find all the dirty places.
        """
        self.path = []

        initial_state = problem.get_initial_state()
        initial_h = initial_state.distance_manhattan(problem.goal_state)
        current_node = AStarNode(initial_state,None,None, 0.0,initial_h)

        priority = current_node.get_cost() + current_node.get_heuristic()
        heapq.heappush(self.frontier, (priority, self.counter, current_node))
        self.counter += 1


        while self.frontier:
            priority, _, current_node = heapq.heappop(self.frontier)
            current_node: AStarNode
            current_state = current_node.get_state()

            
            #Check if we ve reached the goal
            if problem.is_goal_state(current_state):
                #process to do self.path = answer with the parents
                path = []
                node = current_node
                while node is not None:
                    path.append(node)
                    node = node.parent
                path.reverse()
                self.path = path
                return self.path

            # move first frontier to explores 
            self.explored.append(current_node)

            # Get all posibles successors
            successors = problem.get_successors(current_state)

            # add successors to frontier
            for successor in successors:
                h = successor.distance_manhattan(problem.goal_state)
                next_node = AStarNode(
                    successor,
                    current_node,
                    None,
                    current_node.get_cost()+1,
                    h
                )
                heapq.heappush(self.frontier, (h + next_node.get_cost(), self.counter, next_node))
                self.counter += 1
        

            
        return []

    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return [item[2] for item in self.frontier]
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored
    
    def get_all_expanded_nodes(self) -> List[SearchNode]:
        return self.get_explored_nodes() + self.get_frontier_nodes()
    