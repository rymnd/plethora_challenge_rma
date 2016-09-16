#laser cutter - details regarding just the laser cutter system
import laser_geo
import math

#generic laser cutter object
class Cutter(object):
	_v_max		#in/s
	_kerf = 0	#offset kerf (in) (half of the padding given by problem)
	_material_cost = 1	#material cost ($/in^2)
	_machine_cost = 1	#machine time cost ($/s)

	def __init__(self,v_max,kerf,material_cost,machine_cost):
		self._v_max = v_max
		self._kerf = kerf
		self._material_cost = material_cost
		self._machine_cost = machine_cost
	
	#calculate cost when given an edge list (sum of material and machine cost)
	def calculateCost(self,geoArr):
		return self.calculateTime(geoArr)*self._machine_cost + (geoArr.boundingBox.w+self._kerf*2)*(geoArr.boundingBox.h+self._kerf*2) * self._material_cost
		
	#calculate time that machine needs to go through list of geometry elements
	def calculateTime(self,geoArr):
		ts = 0
		for ele in geoArr:
			#check for type and calculate timing appropriately
			if isinstance(ele,laser_geo.Edge):
				ts += self._v_max * ele.L
			elif isinstance(ele,laser_geo.Arc):
				ts += self._v_max * math.exp(-1/ele.radius) * ele.L
			else:
				print "[ERR] Unexpected geometry type: "+repr(type(ele))
		return ts
	
#particular cutter proposed in the Plethora coding challenge
class PlethoraCutter(Cutter):
	def __init__(self):
		Cutter.__init__(self,0.5,0.1/2,0.75,0.07)