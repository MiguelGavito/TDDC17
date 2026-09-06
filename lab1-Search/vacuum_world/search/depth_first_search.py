from typing import List, Set
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch
from collections import deque


class DepthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
        self.path: List[SearchNode] = []
        self.frontier: deque[SearchNode] = deque()
        self.explored = []
        self.visited_states = set()  #We use set for O(1) to get the node directly from the state, instead of O(n) to search in a list.

    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = []
        self.frontier.clear()
        self.explored = []
        self.visited_states.clear()

        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)

        self.frontier.append(current_node)

        while self.frontier:
            current_node: SearchNode = self.frontier.pop() #extract the last node added to the frontier
            current_state = current_node.get_state() 

            if current_state in self.visited_states: #In case the son state has already been explored
                continue

            self.visited_states.add(current_state) # Add the current state to the set of visited states
            self.explored.append(current_node) #store the node in the explored list

            #Check if we have reached the goal state
            if problem.is_goal_state(current_state): 
                path = []
                node = current_node
                while node is not None:
                    path.append(node)
                    node = node.parent
                path.reverse()
                self.path = path
                return self.path

            successors = problem.get_successors(current_state) #Generating the successors
            # add sucessors to frontier
            for successor in successors:
                if successor not in self.visited_states:
                    next_node = SearchNode(successor, current_node, None, current_node.get_cost() + 1)
                    self.frontier.append(next_node)

        return []

    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)

    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored