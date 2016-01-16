from plywood import Plywood,Join
from solid import *

boxlength = 80
boxwidth = 60
boxheight = 20

p = Plywood(boxlength,boxwidth)
p2 = Plywood(boxlength,boxheight)
p3 = Plywood(boxlength,boxheight)
p4 = Plywood(boxheight,boxwidth+.0001)
p5 = Plywood(boxheight,boxwidth+.0001)
p.addCutSides(Join(p2, p, 2))
p.addCutSides(Join(p3, p, 2))
p.addCutSides(Join(p4, p, 1))
p2.addCutSides(Join(p4, p2, 0))
p3.addCutSides(Join(p4, p3, 2))
p.addCutSides(Join(p5, p, 1))
p2.addCutSides(Join(p5, p2, 0))
p3.addCutSides(Join(p5, p3, 2))

parts = []
parts += [p,p2,p3,p4,p5]

scene = union()

scene += p.getSolid()
scene += color([1,0,0])(translate([0,boxwidth/2+0.001,boxheight/2 - 0.001])(rotate(v=[1,0,0], a=90)(p2.getSolid())))
scene += color([0,1,0])(translate([0,-boxwidth/2-0.001+p3.materialsize,boxheight/2 - 0.001])(rotate(v=[1,0,0], a=90)(p3.getSolid())))
scene += color([0,0,1])(translate([boxlength/2 - p4.materialsize,0,p4.width/2-0.001])(rotate(v=[0,1,0], a=90)(p4.getSolid())))
scene += color([0,0,1])(translate([-boxlength/2,0,p4.width/2-0.001])(rotate(v=[0,1,0], a=90)(p5.getSolid())))


for part in parts:
	part.updateCuts()

plan = union()

offset = 0
for part in parts:
	plan.add(translate([0, offset, 0])(part.getSolid()))
	offset += part.height + 5

f = open("test.scad", "w")
f.write(scad_render(plan))
f.close()


