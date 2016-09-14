#2D geometry

class Point(object):
	_x = 0	#should not allow to set publicly
	_y = 0
	
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Edge(object):
	_p1 = None
	_p2 = None

	def __init__(self,p1,p2):
	
class Arc(Edge):
	

	def __init__(self,p1,p2,radius,center):
	
	#return as array of edges
	def discretize(self,dx):
	
class GeoPath():
	edges = None

	def __init__(self,edges):
	
	#return new geopath object w/ offset implemented
	def offset(self,val):
	
	#return rectangle
	def _genBoundingBox(self):
	
	def _genConvexHull(self):
	
	#check that geometry is complete, not self-intersecting, edges connect properly
	def _validate(self):
	
class BoundingBox():
	_w = 0
	_h = 0
	_area = 0
	
	def __init__(self,w,h):
		