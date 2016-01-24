from solid import *


class Join:
	def __init__(self, cutter_plywood, cuts_plywood, side, offset = 0.0, cuts = -1, edge=0):
		self.cutter = cutter_plywood
		self.cuts = cuts_plywood
		self.offset = offset
		self.cuts = cuts
		self.edge = edge
		self.side = side
		self.radius = 2.0005
	
		if ( self.side%2 == 0 ):
			length = self.cutter.width
		else:
			length = self.cutter.height

		if ( self.cuts == -1 ):
			self.cuts = int(2 * length / 80.0+1)
			if ( self.cuts < 2 ):
				self.cuts = 2

	def cutters(self, edge):
		if ( self.side%2 == 0 ):
			length = self.cutter.width
		else:
			length = self.cutter.height

		margin = 0.0
		jump = 0
		step = (length - self.offset) / (self.cuts*2.0-1)
		radius = self.radius + margin

		i_cutv1 = radius
		i_cutv2 = self.cutter.materialsize + 0.01
		if ( self.edge == 1 ):
			i_cutv2 = radius
			i_cutv1 = self.cutter.materialsize + 0.01

		cutters = union()
		for i in range(self.cuts-edge):
			if ( edge == 0 ):
				jump = i
				cuttings = translate([jump*(step-self.offset) + i * (step+self.offset) - margin, -0.005, -0.005])
				cuttings.add(cube([step+margin*2 + self.offset, self.cutter.materialsize + 0.01, self.cutter.materialsize+0.01]))
				if ( i > 0 ):
					cuttings.add(translate([0, self.edge*-radius/2, (1-self.edge) * -radius/2])(cube([radius, i_cutv2,i_cutv1])))
					cuttings.add(translate([0, self.edge*(self.cutter.materialsize-radius/2), (1-self.edge)*(self.cutter.materialsize-radius/2)])(cube([radius, i_cutv2,i_cutv1])))
				if ( i+1 < self.cuts-edge):
					cuttings.add(translate([step+margin*2 + self.offset - radius, self.edge*-radius/2, (1-self.edge)*-radius/2])(cube([radius, i_cutv2,i_cutv1])))
					cuttings.add(translate([step+margin*2 + self.offset - radius, self.edge*(self.cutter.materialsize-radius/2), (1-self.edge)*(self.cutter.materialsize-radius/2)])(cube([radius, i_cutv2,i_cutv1])))
				cutters.add(cuttings)
			else:
				jump = i+1
				cuttings = translate([jump*(step+self.offset) + i * (step-self.offset) - margin, -0.005, -0.005])
				cuttings.add(cube([step+margin*2 - self.offset, self.cutter.materialsize+0.01, self.cutter.materialsize+0.01]))
				cuttings.add(translate([0, (1-self.edge)*-radius/2, self.edge * -radius/2])(cube([radius, i_cutv1, i_cutv2])))
				cuttings.add(translate([0, (1-self.edge)*(self.cutter.materialsize-radius/2),self.edge*(self.cutter.materialsize-radius/2)])(cube([radius, i_cutv1, i_cutv2])))
				cuttings.add(translate([step+margin*2 - self.offset - radius, (1-self.edge)*-radius/2, self.edge*-radius/2])(cube([radius, i_cutv1, i_cutv2])))
				cuttings.add(translate([step+margin*2 - self.offset - radius, (1-self.edge)*(self.cutter.materialsize-radius/2), self.edge*(self.cutter.materialsize-radius/2)])(cube([radius, i_cutv1, i_cutv2])))
				cutters.add(cuttings)

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
