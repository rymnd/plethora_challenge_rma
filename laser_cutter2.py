#laser cutter - details regarding just the laser cutter system
import laser_geo2
import math

#generic laser cutter object
class Cutter(object):
	_v_max		#in/s
	_kerf = 0	#offset kerf (in) (half of the padding)
	_material_cost = 1	#material cost ($/in^2)
	_machine_cost = 1	#machine time cost ($/s)

	def __init__(self,v_max,kerf,material_cost,machine_cost):
		self._v_max = v_max
		self._kerf = kerf
		self._material_cost = material_cost
		self._machine_cost = machine_cost
	
	#calculate cost when given a geometry path (sum of material and machine cost)
	def calculateCost(self,geoPath):
		return self.calculateTime(geoPath)*self._machine_cost + geoPath.boundingBox.area * self._material_cost
		
	#calculate time that machine needs to go through path
	def calculateTime(self,geoPath):
		offset_geoPath = geoPath.offset(self._kerf)
		ts = 0
		for ele in offset_geoPath:
			#check for type and calculate timing appropriately
			if isinstance(ele,laser_geo2.Edge):
				ts += self._v_max * ele.L
			elif isinstance(ele,laser_geo2.Arc):
				ts += self._v_max * math.exp(-1/ele.radius) * ele.L
			else:
				print "[ERR] Unexpected geometry type: "+repr(type(ele))
		return ts
	
#particular cutter proposed in the Plethora coding challenge
class PlethoraCutter(Cutter):
	def __init__(self):
		Cutter.__init__(self,0.5,0.1/2,0.75,0.07)