from typing import List
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch
from collections import deque



class BreadthFirstSearch(BaseSearch):

    def __init__(self):
        """
        Initialize the search algorithm
        """
        super().__init__()

        self.path: List[SearchNode] = []

        # Tailor the following data structures to the needs of the search algorithm
        self.frontier: deque[SearchNode] = deque()
        self.explored = []
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        """
        Perfomr a breath first search to find all the dirty places.
        """
        self.path = []

        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)

        self.frontier.append(current_node)



        while self.frontier:
            
            current_node: SearchNode = self.frontier.popleft()
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
            
            # add succesors to frontier
            for successor in successors:
                next_node = SearchNode(successor,current_node,None,current_node.get_cost() + 1)
                self.frontier.append(next_node)
        
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return self.frontier
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored