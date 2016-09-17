#2D geometry
#avoided using numpy since we're dealing with fairly easy computation
import math

class Point(object):
	x = 0	#should not allow to set publicly
	y = 0
	
	def __init__(self,x,y):
		self.x = round(x,6)	#had some precision issues during testing
		self.y = round(y,6)
	def __eq__(self,other):
		if isinstance(other,self.__class__):
			return self.x==other.x and self.y==other.y
		return False
	
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
	def __eq__(self,other):
		if isinstance(other,self.__class__):
			return self.p1==other.p1 and self.p2==other.p2 and self.L==other.L
		return False
		
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
		ta1 = Point(a.pc.x+dax_1g,a.pc.y+day_1g)
		e1 = Edge(tp1,ta1) if (self.onArc(tp1) and a.onArc(ta1)) else None
		
		#bottom tangent
		dpx_2g = cos_g*dpx-sin_g*(-dpy)
		dpy_2g = sin_g*dpx+cos_g*(-dpy)
		dax_2g = cos_g*dax-sin_g*(-day)
		day_2g = sin_g*dax+cos_g*(-day)
		tp2 = Point(self.pc.x+dpx_2g,self.pc.y+dpy_2g)
		ta2 = Point(a.pc.x+dax_2g,a.pc.y+day_2g)
		e2 = Edge(tp2,ta2) if (self.onArc(tp2) and a.onArc(ta2)) else None
		return [e1,e2]
		
class GeoArr():	#just list of edge elements
	edges = None
	boundingBox = None	
	
	def __init__(self,edges):
		self.edges = edges
		
	#generate smallest area rectangle
	def _genBoundingBox(self):
		self.boundingBox = None
		tangentEdges = []
		#start with existing linear lines
		for ele in self.edges:
			if isinstance(ele,Arc):
				tangentEdges.append(Edge(ele.p1,ele.p2))	#in case of interior curve
				#generate tangent lines between arcs and target points
				for ele2 in self.edges:
					if ele==ele2:	#don't match to itself
						continue
					if isinstance(ele2,Arc):
						tangentPair = ele.tangent2Arc(ele2)
					else:
						#should've remapped p1 and p2 in array instead of explicitly..
						if ele.p1!=ele2.p1 and ele.p2!=ele2.p1:
							tp = ele.tangent2Point(ele2.p1)
							tangentEdges.append(tp[0]) if tp[0] is not None else None 
							tangentEdges.append(tp[1]) if tp[1] is not None else None
						if ele.p1!=ele2.p2 and ele.p2!=ele2.p2:
							tp = ele.tangent2Point(ele2.p2)
							tangentEdges.append(tp[0]) if tp[0] is not None else None 
							tangentEdges.append(tp[1]) if tp[1] is not None else None
				
			elif isinstance(ele,Edge):
				tangentEdges.append(ele)
		
		print repr(len(tangentEdges))+" total tangent edges"
		#should only be edge types
		for tedge in tangentEdges:
			ang = math.acos((tedge.p2.x-tedge.p1.x)/tedge.L)	#for reference, not actually used
			bx = (tedge.p2.x-tedge.p1.x)/tedge.L
			by = (tedge.p2.y-tedge.p1.y)/tedge.L
			tedgeV = tedge.alignV(bx,by)	#should be horizontal now
			
			xmin = min(tedgeV.p1.x,tedgeV.p2.x)
			xmax = max(tedgeV.p1.x,tedgeV.p2.x)
			ymin = tedgeV.p1.y
			ymax = tedgeV.p1.y
			
			isBounding = True
			for ele in self.edges:
				if ele==tedge:
					continue
				#apply reverse rotation to all edges for alignment
				eleV = ele.alignV(bx,by)
				xmin = min(eleV.xmin,xmin)
				xmax = max(eleV.xmax,xmax)
				ymin = min(eleV.ymin,ymin)
				ymax = max(eleV.ymax,ymax)
				
				#check that it is indeed a bounding line - can just check y bounds after alignment - either ymin or ymax should be maintained 
				if ymin<tedgeV.p1.y and ymax>tedgeV.p1.y:
					isBounding = False
					break
			if isBounding:
				tedgeBB = BoundingBox(xmin,xmax,ymin,ymax)
				if self.boundingBox is None or tedgeBB.area<self.boundingBox.area:
					self.boundingBox = tedgeBB
	
class BoundingBox():
	w = 0
	h = 0
	area = 0
	
	xmin = 0
	xmax = 0
	ymin = 0
	ymax = 0
	
	def __init__(self,xmin,xmax,ymin,ymax):
		self.pc = Point((xmax-xmin)/2+xmin,(ymax-ymin)/2+ymin)
		self.w = xmax-xmin
		self.h = ymax-ymin
		self.area = self.w*self.h
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		