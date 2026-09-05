from typing import List
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

    def search(self, problem: SearchProblem) -> List[SearchNode]:
        self.path = []
        self.frontier.clear()
        self.explored = []

        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)

        self.frontier.append(current_node)

        while self.frontier:
            current_node: SearchNode = self.frontier.pop() #extract the last node added to the frontier
            current_state = current_node.get_state() 

            explored_states = [node.get_state() for node in self.explored] #Extracting the states of the explored nodes

            if current_state in explored_states: #In case the son state has already been explored
                continue

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
                next_node = SearchNode(successor, current_node, None, current_node.get_cost() + 1)
                self.frontier.append(next_node)

        return []

    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)

    def get_explored_nodes(self) -> List[SearchNode]:
        return self.explored