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

edge cases:
- applying kerf can make some edges disappear (ie. some petal design)
- for sharp corners, is it better to round that corner instead of continuing the sharp edge w/ offset??

stuff to look up:
- https://en.wikipedia.org/wiki/Minimum_bounding_box_algorithms
- https://en.wikipedia.org/wiki/Convex_hull_algorithms
- http://stackoverflow.com/questions/1109536/an-algorithm-for-inflating-deflating-offsetting-buffering-polygons
    - why is dilation not a thing here?
    - https://en.wikipedia.org/wiki/Straight_skeleton

considerations for extensions, future work
- packing of multiple geometries together (sharing some edge)
- utilizing leftover rectangle stock material
    - determining optimal distribution of rectangle dimensions in stock for some distribution of parts