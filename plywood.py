from solid import *


class Join:
	def __init__(self, cutter_plywood, cuts_plywood, side, offset = 0.0, cuts = 3, edge=0):
		self.cutter = cutter_plywood
		self.cuts = cuts_plywood
		self.offset = offset
		self.cuts = cuts
		self.edge = edge
		self.side = side
		self.radius = 2

	def cutters(self, edge):
		if ( self.side%2 == 0 ):
			length = self.cutter.width
		else:
			length = self.cutter.height


		margin = 0.03
		jump = 0
		step = (length - self.offset) / (self.cuts*2.0-1)
		radius = self.radius + margin

		cutters = union()
		for i in range(self.cuts-edge):
			if ( edge == 0 ):
				jump = i
				cutters.add(translate([jump*(step-self.offset) + i * (step+self.offset) - margin, -0.005, -0.005]) (
					cube([step+margin*2 + self.offset, self.cutter.materialsize + 0.01, self.cutter.materialsize+0.01]),
					translate([0, 0, -radius/2])(cube([radius, self.cutter.materialsize+0.01,radius])),
					translate([0, 0, self.cutter.materialsize-radius/2])(cube([radius, self.cutter.materialsize+0.01,radius])),
					translate([step+margin*2 + self.offset - radius, 0, -radius/2])(cube([radius, self.cutter.materialsize+0.01,radius])),
					translate([step+margin*2 + self.offset - radius, 0, self.cutter.materialsize-radius/2])(cube([radius, self.cutter.materialsize+0.01,radius])))
				)
			else:
				jump = i+1
				cutters.add(translate([jump*(step+self.offset) + i * (step-self.offset) - margin, -0.005, -0.005]) (
					cube([step+margin*2 - self.offset, self.cutter.materialsize+0.01, self.cutter.materialsize+0.01]),
					translate([0, -radius/2, 0])(cube([radius, radius, self.cutter.materialsize+0.01])),
					translate([0, self.cutter.materialsize-radius/2,0])(cube([radius, radius, self.cutter.materialsize+0.01])),
					translate([step+margin*2 + self.offset - radius, -radius/2, 0])(cube([radius, radius, self.cutter.materialsize+0.01])),
					translate([step+margin*2 + self.offset - radius, self.cutter.materialsize-radius/2, 0])(cube([radius, radius, self.cutter.materialsize+0.01])))
				)

		return cutters

class Plywood:
	def __init__(self, width, height, materialsize=4.2):
		self.width = float(width)
		self.height = float(height)
		self.materialsize = float(materialsize)
		self.joinedPlywood = []
		self.cuts = []
		self.cube = None

		self.solid = translate([-self.width/2, -self.height/2, 0])

	def addCutSides(self, cut):
		self._addCutSides(cut)
		if( cut.cutter == self ):
			cut.cuts._addCutSides(cut)
		else:
			cut.cutter._addCutSides(cut)
	
	def _addCutSides(self, cut):
		self.cuts += [cut]

	def sideTranslation(self, cut, cutters):
		if ( cut.side == 0 ):
			return translate([0, self.height - self.materialsize, 0])(cutters)
		if ( cut.side == 1 ):
			return translate([self.width, 0, 0])(rotate(v=[0,0,1], a=90)(cutters))
		if ( cut.side == 2 ):
			return translate([0, 0, 0])(cutters)
		if ( cut.side == 3 ):
			return translate([0 + self.materialsize, 0, 0])(rotate(v=[0,0,1], a=90)(cutters))

		return None

	def updateCuts(self):
		for cut in self.cuts:
			if cut.cutter == self:
				edge = 1 - cut.edge
			else:
				edge = cut.edge

			cutters = cut.cutter.sideTranslation(cut, cut.cutters(edge))
			if ( cut.cutter != self ):
				heap = []
				obj = cut.cutter.cube.parent
				while ( obj != None ):
					heap = heap + [obj]
					obj = obj.parent

				for obj in heap:
					if isinstance(obj, translate):
						cutters = translate(obj.params['v'])(cutters)
					if isinstance(obj, rotate):
						cutters = rotate(v = obj.params['v'], a = obj.params['a'])(cutters)

				obj = self.cube.parent
				heap = []
				while ( obj != None ):
					heap = [obj] + heap
					obj = obj.parent
				for obj in heap:
					if isinstance(obj, translate):
						cutters = translate([-obj.params['v'][0], -obj.params['v'][1], -obj.params['v'][2]])(cutters)
					if isinstance(obj, rotate):
						cutters = rotate(v=obj.params['v'], a=-obj.params['a'])(cutters)
					obj = obj.parent

			self.cube.add(cutters)

	def getSolid(self):
		if ( self.cube != None ):
			return self.cube
		self.cube = difference()(cube([self.width, self.height, self.materialsize]))
		self.solid.add(self.cube)

		return self.solid
