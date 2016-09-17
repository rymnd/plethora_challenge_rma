#laser cutter system - handles profile deserialization, user interaction
import laser_geo
import laser_cutter
import json
import sys

#made this a separate object (even though it serves just as a container) in case profiles/orders in future may have additional characteristics/demands (like finishing, post-processing, etc)
class Profile(object):
	_jsonEdges = None
	_jsonVertices = None
	
	vertices = None
	edges = None
	geoArr = None
	
	def __init__(self,jsonText):
		jsonObj = json.loads(jsonText)	#assume that the json file is valid
		self._jsonEdges = jsonObj['Edges']
		self._jsonVertices = jsonObj['Vertices']	#only needed for reference
		
		self.vertices = []
		for k,v in self._jsonVertices.iteritems():
			self.vertices.append(laser_geo.Point(v['Position']['X'],v['Position']['Y']))
		
		#order in path not important for stock challenge - just create geometry type and store in array
		self.edges = []
		for k,v in self._jsonEdges.iteritems():
			p1_id = str(v['Vertices'][0])
			p1 = laser_geo.Point(self._jsonVertices[p1_id]['Position']['X'],self._jsonVertices[p1_id]['Position']['Y'])
			p2_id = str(v['Vertices'][1])
			p2 = laser_geo.Point(self._jsonVertices[p2_id]['Position']['X'],self._jsonVertices[p2_id]['Position']['Y'])
			
			if v['Type']=='LineSegment':
				self.edges.append(laser_geo.Edge(p1,p2))
			elif v['Type']=='CircularArc':
				pc = laser_geo.Point(v['Center']['X'],v['Center']['Y'])
				if v['ClockwiseFrom']==v['Vertices'][0]:
					self.edges.append(laser_geo.Arc(p1,p2,pc))
				else:
					self.edges.append(laser_geo.Arc(p2,p1,pc))
		self.geoArr = laser_geo.GeoArr(self.edges,self.vertices)
class PlethoraSystem(object):
	_cutter = None
	_profile = None
	
	def __init__(self,cutter):
		self._cutter = cutter
		
	def calculateCost(self,fileName):
		self._processProfile(fileName)
		return self._cutter.calculateCost(self._profile.geoArr)
		
	def _processProfile(self,fileName):
		f = open(fileName,'r')
		self._profile = Profile(f.read())
		
if __name__=="__main__":
	ps = PlethoraSystem(laser_cutter.PlethoraCutter())
	if len(sys.argv)>1:
		fname = sys.argv[1]
		cost = ps.calculateCost(fname)
		print "Cost for "+repr(fname)+": $"+repr(round(cost,2))
	