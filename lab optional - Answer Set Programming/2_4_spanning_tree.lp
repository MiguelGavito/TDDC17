% Lab 3.2.4: Spanning Tree Problem

% Test instance
edge(1,2). edge(2,3). edge(1,4). edge(2,5). edge(3,6). edge(4,5). 
edge(5,6). edge(1,5). edge(2,6). edge(3,7). edge(6,7).

edge(X,Y) :- edge(Y,X).
vertex(X) :- edge(X,_).

