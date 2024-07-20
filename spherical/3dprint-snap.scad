
use <2tri1tri_alt.scad>;

r=75;
w=8;
h=8;
e=.001;

use <snap.scad>;


module shape()
{
difference()
{
union(){
both_sides()translate([r-h/2,w/3,-w/2])rotate([0,0,180])hook(h, 4, 4.5, 1, .75, 1.5, 4);
chopped_arc(r,w,h);
}

both_sides()step_x()translate([r-h/2,w/3,-w/2])rotate([0,0,180])latch(h, 4, 4.5, 1, .75, 1.5, 4, .2, .2);
}
}

module test()
{
    difference()
    {
    shape();

union(){
for (i=[1,3,5])rotate([0,0,i/6*159])translate([75,0,0])cube([40,40,40],center=true);
}
}}

//ball()
shape();

//test();
