from solid import *


class Join:
	def __init__(self, cutter_plywood, cuts_plywood, offset = 0, cuts = 3, edge=0, side=0):
		self.cutter = cutter_plywood
		self.cuts = cuts_plywood
		self.offset = offset
		self.cuts = cuts
		self.edge = edge

	def cutters(self, edge, offset=0.0):
		if ( side%2 == 0 ):
			length = self.cutter.width
		else:
			lenght = self.cutter.height


		margin = 0.03
		jump = 0
		step = (length - self.offset) / (self.cuts*2.0-1)

		cutters = union()
		for i in range(self.cuts-edge):
			if ( edge == 0 ):
				jump = i
				cutters.add(translate([jump*(step-self.offset) + i * (step+self.offset) - margin, -0.005, -0.005]) (
					cube([step+margin*2 + self.offset, self.cutter.materialsize + 0.01, self.cutter.materialsize+0.01]))
				)
			else:
				jump = i+1
				cutters.add(translate([jump*(step+self.offset) + i * (step-self.offset) - margin, -0.005, -0.005]) (
					cube([step+margin*2 - self.offset, self.cutter.materialsize+0.01, self.cutter.materialsize+0.01]))
				)

		return cutters

class Plywood:
	def __init__(self, width, height, materialsize=4.2):
		self.width = float(width)
		self.height = float(height)
		self.materialsize = float(materialsize)
		self.joinedPlywood = []
		self.cuts = []
		self.move = union()

	def __str__(self):
		print "Plywood..."

	def cutby(self, plywood):
		self.joinedPlywood += [plywood]

	def addCutSides(self, cut):
		self._addCutSides(cut)
		if( cut.cutter == self ):
			cut.cuts._addCutSides(cut)
		else:
			cut.cutter._addCutSides(cut)
	
	def _addCutSides(self, cut):
		self.cuts += [cut]

	def vaneCutter(self, length, material, count, edge, offset=0.0):
		margin = 0.03
		jump = 0
		step = (length - offset) / (count*2.0-1)

		cutters = union()
		for i in range(count-edge):
			if ( edge == 0 ):
				cutters.add(translate([jump*(step-offset) + i * (step+offset) - margin, -0.005, -0.005]) (cube([step+margin*2 + offset, material + 0.01, material+0.01])))
				jump = i+1
			else:
				jump = i+1
				cutters.add(translate([jump*(step+offset) + i * (step-offset) - margin, -0.005, -0.005]) (cube([step+margin*2 - offset, material+0.01, material+0.01])))

		return cutters

	def getCutters(self):
		ret = union()
		cuts = 3
		ret.add(translate([-self.width/2, -self.height/2,0])(self.vaneCutter(self.width, self.materialsize, cuts, 1)))
		ret.add(translate([-self.width/2, self.height/2 - self.materialsize,0])(self.vaneCutter(self.width, self.materialsize, cuts, 1)))
		ret.add(translate([-self.width/2 + self.materialsize, -self.height/2,0])(
			rotate(v=[0,0,1],a=90)(self.vaneCutter(self.height, self.materialsize, 2, 1)))
		)
		ret.add(translate([self.width/2, -self.height/2,0])(
			rotate(v=[0,0,1],a=90)(self.vaneCutter(self.height, self.materialsize, 2, 0)))
		)

		return ret;

	def getSolid(self):
		ret = translate([-self.width/2, -self.height/2, 0])(
			cube([self.width, self.height, self.materialsize])
		)
		for plywood in self.joinedPlywood:
			ret -= plywood.getCutters()
		return ret
