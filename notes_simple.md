simplified notes for Plethora challenge now that I've actually read the challenge properly - 5:16pm, Fri, Sept 16 =(

CORRECTIONS:
	- padding ONLY applies to the stock material, not the actual cut

simplified geometry problem:
	- don't need to worry about order of edges
		- can treat each of them as independent path component
		- only care about length and type of edge to calculate the cutting time
	- only need to find bounding box of given geometry
		- for arcs, find tangents to all other points >> use as test lines for bounding box >> otherwise still the same bounding box algorithm
		- don't need to account for cutting time of box, just the modified area w/ padding
	- arcs:
		- only need to calculate tangents for convex arcs curving outwards
		- arcs curving inwards can be replaced by edge during calculation of bounding box
		- http://mathoverflow.net/questions/93659/find-the-bounding-box-of-a-circle-segment
			- bounding box for an arc (to help w/ overall bounding box calculation)
		- tangent to point/arc subproblems
			- http://mathworld.wolfram.com/Circle-CircleTangents.html
			- 