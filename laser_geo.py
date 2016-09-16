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
	#determines if provided point is on right of edge (1:right,0:on,-1:left)
	def whichSide(self,p):
		return (p.x-p1.x)*(p2.y-p1.y) - (p.y-p1.y)*(p2.x-p1.x)
	
class Arc(Edge):
	pc = None	#arc center
	radius = 0
	ang = #angle of arc
	
	#assume that p1 is starting point for clockwise arc
	def __init__(self,p1,p2,center):
		self.pc = center
		self.radius = ((p1.x-center.x)**2+(p1.y-center.y)**2)**0.5
		Edge.__init__(self,p1,p2)	#assume that p1 is starting point of arc
		
		#arc length (2 options, may need to reverse)
		if whichSide(self.pc)==0:
			self.ang = math.pi
		else:
			self.ang = 2.*math.asin((0.5*self.L) / self.radius)	#shorter angle
			if (whichSide(self.pc)<0):	#center on left of given endpoints
				self.ang = math.pi*2 - self.ang
		self.L = self.ang * self.radius

class GeoArr():	#just list of edge elements
	edges = None
	boundingBox = None	#width,height and center
	
	def __init__(self,edges):
		self.edges = edges
		
	#generate smallest area rectangle
	def _genBoundingBox(self):
		#generate tangent lines if arcs exist
		
		#only keep tangent lines if all other points are on one side of the line
	
		#for each line, calculate the aligned rectangle area
		
			#apply rotation to all edges for alignment
			
			#construct bounding box
			
		self.boundingBox = BoundingBox(Point(0,0),5.,5.)
	
class BoundingBox():
	w = 0
	h = 0
	area = 0
	
	def __init__(self,pc,w,h):
		self.pc = pc
		self.w = w
		self.h = h
		self.area = w*h