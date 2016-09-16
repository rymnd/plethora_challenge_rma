#laser cutter system - handles profile deserialization, user interaction
import laser_geo2
import laser_cutter2
import json

class Profile(object):
	_jsonEdges = None
	_jsonVertices = None
	_vertices = None
	_edges = None
	geoPath = None
	
	def __init__(self,jsonText):
		jsonObj = json.loads(jsonText)	#assume that the json file is valid
		self._jsonEdges = jsonObj['Edges']
		self._jsonVertices = jsonObj['Vertices']	#only needed for reference
		
		#want to put elements in path order
		for k,v in self._jsonEdges.iteritems():
	
	
class PlethoraSystem(object):
	_cutter = None
	_profile = None
	
	def __init__(self,cutter):
		self._cutter = cutter
	
	def processProfile(self,fileName):
		f = load(fileName)
		self._profile = Profile(f.read())