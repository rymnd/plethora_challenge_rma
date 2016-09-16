Plethora Technical Challenge Notes

https://gist.github.com/mrivlin/4bd6f29bedaec07b8e36

steps:
- deserialize json representation into code representation
    - need classes for different edge types
    - each edge type is just some direct move w/ some cost
- want geometric representation to find enclosing polygon/rectangle
    - just need to deal w/ circular edges somehow (approximation not ideal)
    - infinite possibilities for how to align rectangle edge w/ circle??
        - convex hull should be enough
    - need to apply offset to handle the laser cutter kerf >> actual cut on the outer edge

classes
- system (integrator)
    - decodeProfile
- geometry (direct from profile)
    - edge >> arc
    - output bounding rectangle
    - output_offset (generate new geometry object)
- geometry_offset 
    - offset_val
    - geometry (base path)
- profile (or interpreter)
    - instantiated by json or accepts json as primary argument
- cutter
    - costs
    - speed 
    - kerf (offset value)
    - process_geometry

unpacking and ordering edges:
	- edges not necessarily in proper order
	- each edge not necessarily w/ vertices in clockwise order
	- O(VE): for each vertex, find the next edge
	- O(E^2): each edge traversed once, need to find 
	
edge cases:
- applying kerf can make some edges disappear (ie. some petal design)
- for sharp corners, is it better to round that corner instead of continuing the sharp edge w/ offset??

confusion/concerns about arcs:
	- 4 possible cases (in either direction, long or short arc)
	- radius either shrunk or extended to account for kerf (depends on orientation)
	- need to calculate tangent lines in calculating hull 
		- where to terminate these tangent lines??
		- in testing convex hull, what point on arc to choose??
	- each arc needs a parameterized tangent line equation?
	- if arc bends to the right (overall clockwise path), we don't care from convex hull or bounding box perspective
		- can just use end points and use straight edge
	- https://algnotes.wordpress.com/2013/12/13/convex-hull-of-circles/
		- center MUST be on hull for circle to be part of hull
		- for arcs, can start w/ circle calculation, then check w/ arc endpoints
	- http://stackoverflow.com/questions/1336663/2d-bounding-box-of-a-sector
		- arc bounding box is easy if we start w/ a known alignment
		- what happens if all line segments are not part of hull??
			- how do we check for this possibility?
		
tangent line properties in arcs:
	- always perpendicular to radii in both arc definitions
	- between 2 circles, can always find points of tangency w/ just centers and radii
		
stuff to look up:
- https://en.wikipedia.org/wiki/Minimum_bounding_box_algorithms
	- check each edge (from hull) >> MUST have an edge collinear w/ one of the hull edges
- https://en.wikipedia.org/wiki/Convex_hull_algorithms
	- IMPORTANT: for this challenge, the correctness of the convex hull doesn't matter >> only used to find the bounding rectangle
		- maybe it's ok to preserve the curves (rectangle edge just tangent to arc)
	- http://www.cs.uu.nl/docs/vakken/ga/slides1.pdf (slow brute force method for hull)
		- SLOWCONVEXHULL: for each pair of points, make edge and check if all other points lie on one side of it
		- INCREMENTAL: in some global cartesian direction, can always pick one point to start (guaranteed to be on the convex hull)
			- split into upper and lower convex hull pieces
			- remove previous line if direction of line changes in some direction (go clockwise!)
		- other ideas: 
			- divide and conquer (if smaller components have simpler convex hulls)
				- how to merge different hulls? (not described)
				- split arcs and edges >> find 2 sets of hulls, then combine
			- deflate/inflate circles (start with circle centers)
				- hull of circles always include the arc, linear segments determined by tangency lines
		- QuickHull: eliminate interior points as quickly/early as possible
			- can always start w/ 4 points at max/min cartesian directions
- http://stackoverflow.com/questions/1109536/an-algorithm-for-inflating-deflating-offsetting-buffering-polygons
    - why is dilation not a thing here?
    - https://en.wikipedia.org/wiki/Straight_skeleton
	- "polygon-buffering"
	- also same problem as minkowski sum of polygon path and circle, but then need to find the outer contour >> minkowski usually falls back onto discretization

considerations for extensions, future work
- packing of multiple geometries together (sharing some edge)
- utilizing leftover rectangle stock material
    - determining optimal distribution of rectangle dimensions in stock for some distribution of parts