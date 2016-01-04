from plywood import Plywood
from solid import *

p = Plywood(60,40)
p2 = Plywood(40,30)
p.cutby(p2)


f = open("test.scad", "w")
f.write(scad_render(p.getSolid() + translate([0,0,-1])(p2.getSolid().set_modifier("debug"))))
f.close()


