# Plethora Challenge - Raymond Ma

Basic Usage:
python laser_system.py [json filepath]

> python laser_system.py challenge_json/Rectangle.json

========
# Approach Summary

- for each edge element, calculate total length and associated bounding box
	- type and length are sufficient to calculate machine time on that edge
- for each arc, calculate tangent lines to other points and other arcs
	- may need to use these tangent lines to find bounding box 
- for each line segments and tangent lines, re-orient all edges to new coordinate frame established by the line being tested
	- bounding boxes of all re-oriented edges should lie on one side of the line being tested for that line to establish a valid bounding box
	- iterate through all possibilities and output bounding box with smallest area

========

# Notes/Considerations

- avoided all but the most basic additional libraries (math and json)
	- assumed you didn't want me to re-implement json deserialization from scratch, but maybe sorry if I got that wrong
- had originally misread the prompt that thought the padding/kerf needed to be assigned to the given profile, not just the bounding box
	- the *2.py files and notes.md reflect my thought process for that particular application
- didn't think I needed to evaluate the convex hull
	- with the arc representation without discretization, the convex hull would have needed to maintain the arc
	- though this would have helped with concave features

========

# Would have liked to...

- avoid trigonometric functions entirely if possible
	- basis vectors alone should have been enough for the transformations used
- improve the time/space complexity of the problem
	- for rotations, I just generated a new edge object everytime. Could've just done rotations in place
	- ordering the profile elements in a path (or structuring the list better) may have improved time complexity
	- the bulk of calculated tangent lines and edge lines for geometries with concave features likely don't need to be evaluated for the bounding box
	- definitely doubling up on arc-arc tangent lines that are calculated/tested
	- should have tried divide/conquer technique with the geometry
		- find convex hull for non-arc line segments/vertices, then combine that convex hull with the system arcs
- explore more edge cases
	- ie. flower petal geometry composed of only arcs, star/concave shapes where none of original line segments are collinear with the bounding box lines