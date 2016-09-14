#laser cutter - details regarding just the laser cutter system
import laser_geo

#generic laser cutter object
class Cutter(object):
	_v_max		#in/s
	_kerf = 0	#offset kerf (in)
	_material_cost = 1	#material cost ($/in^2)
	_machine_cost = 1	#machine time cost ($/s)

	def __init__(self,v_max,kerf,material_cost,machine_cost):
	
	#calculate cost when given a geometry path (sum of material and machine cost)
	def calculateCost(self,geoPath):
		return self.calculateTime(geopath)*self._machine_cost + geoPath.boundingBox.area * self._material_cost
		
	#calculate time that machine needs to go through path
	def calculateTime(self,geoPath):
	
#particular cutter proposed in the Plethora coding challenge
class PlethoraCutter(Cutter):
	def __init__(self):
		Cutter.__init__(self,0.5,0.1,0.75,0.07)