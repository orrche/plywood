from plywood import Plywood,Join
from solid import *

p = Plywood(60,40)
p2 = Plywood(40,30)
# p.cutby(p2)
p.addCutSides(Join(p2, p, 0))
p.addCutSides(Join(p2, p, 1))
p.addCutSides(Join(p2, p, 2))
p.addCutSides(Join(p2, p, 3))


scene = union()

scene += p.getSolid()
scene += translate([0,0,-1])(p2.getSolid())

p.updateCuts()
p2.updateCuts()

f = open("test.scad", "w")
f.write(scad_render(scene))
f.close()


