% Lab 3.2.2: Dominating Set Problem

% Test instance
edge(1,2). edge(2,3). edge(3,4). edge(4,5). edge(5,1).

edge(X,Y) :- edge(X,Y).
vertex(X) :- edge(X, _).

% Setting k=2, but feel free to change this when testing
k_bound(2).
