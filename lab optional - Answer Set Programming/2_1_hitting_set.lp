% Lab 3.2.1: Hitting Set Problem

% Test instance
subset(s1, 1). subset(s1, 2). subset(s1, 5).
subset(s2, 2). subset(s2, 3). subset(s2, 5).
subset(s3, 3). subset(s3, 4). subset(s3, 6).
subset(s4, 1). subset(s4, 4).

% Get all elements names
element(X) :- subset(_, X).

% Get all subset names
subset_name(S) :- subset(S, _).

% Set k=2, but feel free to change this when testing
k_bound(2).
