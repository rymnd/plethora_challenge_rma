#2D geometry
#avoided using numpy since we're dealing with fairly easy computation
import math

class Point(object):
	x = 0	#should not allow to set publicly
	y = 0
	
	def __init__(self,x,y):
		self.x = round(x,6)	#had some precision issues during testing
		self.y = round(y,6)
	
class Edge(object):
	p1 = None
	p2 = None
	L = 0	#length
	
	xmin = 0
	xmax = 0
	ymin = 0
	ymax = 0
	
	def __init__(self,p1,p2):
		self.p1 = p1
		self.p2 = p2
		self.L = ((self.p2.x-self.p1.x)**2+(self.p2.y-self.p1.y)**2)**0.5
		self.xmin = min(p1.x,p2.x)	#limits to help with bounding box calculation
		self.xmax = max(p1.x,p2.x)
		self.ymin = min(p1.y,p2.y)
		self.ymax = max(p1.y,p2.y)
		
	#determines if provided point is on right of edge (1:right,0:on,-1:left)
	def whichSide(self,p):
		return (p.x-self.p1.x)*(self.p2.y-self.p1.y) - (p.y-self.p1.y)*(self.p2.x-self.p1.x)
		
	def rotate(self,ang):
		p1 = Point(math.cos(ang)*self.p1.x - math.sin(ang)*self.p1.y,math.sin(ang)*self.p1.x + math.cos(ang)*self.p1.y)
		p2 = Point(math.cos(ang)*self.p2.x - math.sin(ang)*self.p2.y,math.sin(ang)*self.p2.x + math.cos(ang)*self.p2.y)
		return Edge(p1,p2)
		
	#rotation when given basis vector >> rotate such that given [bx by] is new x-axis
	def alignV(self,bx,by):
		p1 = Point(bx*self.p1.x+by*self.p1.y, -by*self.p1.x+bx*self.p1.y)
		p2 = Point(bx*self.p2.x+by*self.p2.y, -by*self.p2.x+bx*self.p2.y)
		return Edge(p1,p2)
	
class Arc(Edge):
	pc = None	#arc center
	radius = 0
	ang = 0 #angle of arc
	
	#assume that p1 is starting point for clockwise arc
	def __init__(self,p1,p2,center):
		self.pc = center
		self.radius = round(((p1.x-center.x)**2+(p1.y-center.y)**2)**0.5,6)
		Edge.__init__(self,p1,p2)	#assume that p1 is starting point of arc
		
		#arc length (2 options, may need to reverse)
		if self.whichSide(self.pc)==0:
			self.ang = math.pi
		else:
			self.ang = 2.*math.asin((0.5*self.L) / self.radius)	#shorter angle
			if (self.whichSide(self.pc)<0):	#center on left of given endpoints
				self.ang = math.pi*2 - self.ang
		self.L = self.ang * self.radius
		
		#possible limits:
		validx = [self.p1.x, self.p2.x]
		validy = [self.p1.y, self.p2.y]
		for mxy in [[1,0],[0,1],[-1,0],[0,-1]]:
			cx = self.pc.x+mxy[0]*self.radius
			cy = self.pc.y+mxy[1]*self.radius
			if self.onArc(Point(cx,cy)):
				validx.append(cx)
				validy.append(cy)
		self.xmin = min(validx)
		self.xmax = max(validx)
		self.ymin = min(validy)
		self.ymax = max(validy)
		
	def rotate(self,ang):
		p1 = Point(math.cos(ang)*self.p1.x - math.sin(ang)*self.p1.y,math.sin(ang)*self.p1.x + math.cos(ang)*self.p1.y)
		p2 = Point(math.cos(ang)*self.p2.x - math.sin(ang)*self.p2.y,math.sin(ang)*self.p2.x + math.cos(ang)*self.p2.y)
		pc = Point(math.cos(ang)*self.pc.x - math.sin(ang)*self.pc.y,math.sin(ang)*self.pc.x + math.cos(ang)*self.pc.y)
		return Arc(p1,p2,pc)
	def alignV(self,bx,by):
		p1 = Point(bx*self.p1.x+by*self.p1.y, -by*self.p1.x+bx*self.p1.y)
		p2 = Point(bx*self.p2.x+by*self.p2.y, -by*self.p2.x+bx*self.p2.y)
		pc = Point(bx*self.pc.x+by*self.pc.y, -by*self.pc.x+bx*self.pc.y)
		return Arc(p1,p2,pc)
	#whether point is found on the given arc
	def onArc(self,p):
		pdist = round(((p.x-self.pc.x)**2+(p.y-self.pc.y)**2)**0.5, 6)
		if pdist!=self.radius:
			return False
		#check that point is between the starting and end points (on proper side)
		return self.whichSide(p) <= 0
	
	#returns up to 2 lines tangent to arc and a given point
	def tangent2Point(self,p):
		pdist = ((p.x-self.pc.x)**2+(p.y-self.pc.y)**2)**0.5	#center to p distance
		#edge case: cannot have one if point is within the circle
		if pdist<=self.radius:
			return [None,None]
		tL = ((pdist)**2-self.radius**2)**0.5	#length of the tangent line
		# cang = math.acos(self.radius/pdist)	#angle between radius and pdist line
		# pgang = math.asin((p.y-self.pc.y) / pdist) #global angle for vector to p
		# tp1 = Point(self.pc.x+math.cos(pgang+cang)*self.radius, self.pc.y+math.sin(pgang+cang)*self.radius)
		# tp2 = Point(self.pc.x+math.cos(pgang-cang)*self.radius, self.pc.y+math.sin(pgang-cang)*self.radius)
		
		# better to deal in ratios than trig functions?
		cos_t = self.radius/pdist
		sin_t = tL/pdist
		cos_g = (p.x-self.pc.x) / pdist	#global adjustment
		sin_g = (p.y-self.pc.y) / pdist
		
		dx1 = self.radius*cos_t
		dy1 = self.radius*sin_t
		dx2 = self.radius*cos_t
		dy2 = self.radius*-sin_t
		
		dx_1g = cos_g*dx1-sin_g*dy1
		dy_1g = sin_g*dx1+cos_g*dy1
		dx_2g = cos_g*dx2-sin_g*dy2
		dy_2g = sin_g*dx2+cos_g*dy2
		
		tp1 = Point(self.pc.x+dx_1g,self.pc.y+dy_1g)
		tp2 = Point(self.pc.x+dx_2g,self.pc.y+dy_2g)
		
		e1 = Edge(tp1,p) if self.onArc(tp1) else None
		e2 = Edge(tp2,p) if self.onArc(tp2) else None
		return [e1,e2]
		
	def tangent2Arc(self,a):
		#find the 2 lines tangent to both circles, then check that endpoints are on the arc
		cdist = ((self.pc.x-a.pc.x)**2+(self.pc.y-a.pc.y)**2)**0.5
		cdx = a.pc.x-self.pc.x
		cdy = a.pc.y-self.pc.y 
		#cos = cdx/cdist, sin = cdy/cdist
		cos_g = cdx/cdist
		sin_g = cdy/cdist
		
		dr = self.radius-a.radius
		tL = (cdist**2-(dr)**2)**0.5
		#cos = dr/cdist, sin = tL/cdist
		cos_t = dr/cdist
		sin_t = tL/cdist
		
		#avoiding trig functions here to find offset
		dpx = self.radius*cos_t
		dpy = self.radius*sin_t
		dax = a.radius*cos_t
		day = a.radius*sin_t
		
		#top tangent
		dpx_1g = cos_g*dpx-sin_g*dpy
		dpy_1g = sin_g*dpx+cos_g*dpy
		dax_1g = cos_g*dax-sin_g*day
		day_1g = sin_g*dax+cos_g*day
		tp1 = Point(self.pc.x+dpx_1g,self.pc.y+dpy_1g)
		ta1 = Point(a.x+dax_1g,a.y+day_1g)
		e1 = Edge(tp1,ta2) if (self.onArc(tp1) and a.onArc(ta1)) else None
		
		#bottom tangent
		dpx_2g = cos_g*dpx-sin_g*(-dpy)
		dpy_2g = sin_g*dpx+cos_g*(-dpy)
		dax_2g = cos_g*dax-sin_g*(-day)
		day_2g = sin_g*dax+cos_g*(-day)
		tp2 = Point(self.pc.x+dpx_2g,self.pc.y+dpy_2g)
		ta2 = Point(a.x+dax_2g,a.y+day_2g)
		e2 = Edge(tp2,ta2) if (self.onArc(tp2) and a.onArc(ta2)) else None
		return [e1,e2]
		
class GeoArr():	#just list of edge elements
	edges = None
	boundingBox = None	#width,height and center
	
	def __init__(self,edges):
		self.edges = edges
		
	#generate smallest area rectangle
	def _genBoundingBox(self):
		tangentEdges = []
		#start with existing linear lines
		# for edge in self.edges:
			# if isinstance(edge,laser_geo.Edge):
				# tangentEdges.append(edge)
			# elif isinstance(edge,laser_geo.Arc):
				# #generate tangent lines if arcs exist
		
				# #only keep tangent lines if all other points are on one side of the line
		# for tedge in tangentEdges:
		#for each line, calculate the aligned rectangle area
		
			#apply rotation to all edges for alignment
			
			#construct bounding box
			
		self.boundingBox = BoundingBox(Point(0,0),5.,5.)
	
class BoundingBox():
	w = 0
	h = 0
	area = 0
	
	xmin = 0
	xmax = 0
	ymin = 0
	ymax = 0
	
	def __init__(self,pc,w,h):
		self.pc = pc
		self.w = w
		self.h = h
		self.area = w*h
		self.xmin = self.pc.x-self.w/2.
		self.xmax = self.pc.x-self.w/2.
		self.ymin = self.pc.y-self.h/2.
		self.ymax = self.pc.y-self.h/2.
		