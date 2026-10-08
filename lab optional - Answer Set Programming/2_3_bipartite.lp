% Lab 3.2.3: Bipartite Graph Testing

% Test instance 1
% edge(1,2). edge(2,3). edge(3,4). edge(4,1).

% Test instance 2
edge(1,2). edge(2,3). edge(3,1).

edge(X,Y) :- edge(X,Y).
vertex(X) :- edge(X, _).
