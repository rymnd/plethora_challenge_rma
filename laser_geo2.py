#2D geometry
#avoided using numpy since we're dealing with fairly easy computation
import math

class Point(object):
	x = 0	#should not allow to set publicly
	y = 0
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
	
class Edge(object):
	p1 = None
	p2 = None
	L = 0	#length
	
	def __init__(self,p1,p2):
		self.p1 = p1
		self.p2 = p2
		self.L = ((self.p2.x-self.p1.x)**2+(self.p2.y-self.p1.y)**2)**0.5
	#determines if provided point is on right of edge (>0:right,0:on,<0:left)
	def whichSide(self,p):
		return (p.x-p1.x)*(p2.y-p1.y) - (p.y-p1.y)*(p2.x-p1.x)
	
class Arc(Edge):
	pc = None	#arc center
	radius = 0
	ang = #angle of arc
	pa1 = None	#arc control points (may be used for convex hull)
	pa2 = None
	dir = True	#True: right, False: left
	
	def __init__(self,p1,p2,radius,center,dir=True):
		self.radius = radius
		self.pc = center
		self.dir = dir
		Edge.__init__(self,p1,p2)	#assume that p1 is starting point of arc
		
		#arc length (2 options, may need to reverse)
		
		if whichSide(self.pc)==0:
			self.ang = math.pi
		else:
			self.ang = 2.*math.asin((0.5*self.L) / self.radius)	#shorter angle
			if (whichSide(self.pc)>0 and self.dir) or (whichSide(self.pc)<0 and not self.dir):
				self.ang = math.pi*2 - self.ang
		self.L = self.ang * self.radius
				
	#return as array of edges (for debugging purposes)
	def discretize(self,N):
		return None
	
class GeoPath():	#continuous clockwise path so we can step through in sequence
	segments = None
	boundingBox = None	#width,height and center
	convexHull = None	#array of points in clockwise order
	
	def __init__(self,segments):
		self.segments = segments
	
	#return new geopath object w/ offset implemented
	def offset(self,val):
		return None
		
	#return rectangle
	def _genBoundingBox(self):
		return None
	
	def _genConvexHull(self):
		return None
	
	#check that geometry is complete, not self-intersecting, edges connect properly
	def _validate(self):
		return True
	
class BoundingBox():
	w = 0
	h = 0
	area = 0
	
	def __init__(self,pc,w,h):
		self.pc = pc
		self.w = w
		self.h = h
		self.area = w*h