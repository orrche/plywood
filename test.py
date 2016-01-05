from plywood import Plywood,Join
from solid import *

p = Plywood(60,40)
p2 = Plywood(60,30)
p3 = Plywood(60,30)
p4 = Plywood(30,40.0001)
p5 = Plywood(30,40.0001)
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
scene += color([1,0,0])(translate([0,40/2+0.001,30/2 - 0.001])(rotate(v=[1,0,0], a=90)(p2.getSolid())))
scene += color([0,1,0])(translate([0,-40/2-0.001+p3.materialsize,30/2 - 0.001])(rotate(v=[1,0,0], a=90)(p3.getSolid())))
scene += color([0,0,1])(translate([15,0,p4.width/2-0.001])(rotate(v=[0,1,0], a=90)(p4.getSolid())))
scene += color([0,0,1])(translate([-15,0,p4.width/2-0.001])(rotate(v=[0,1,0], a=90)(p5.getSolid())))


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


