
use <2tri1penta_alt.scad>;

/*
module dowel(diameter, length){
    translate([0,length/2,0])rotate([90,0,0]) cylinder(length, r=diameter/2, center=true, $fn=20);
}
*/

r=200;
w=12;
h=12;
e=.001;

union()
{
    chopped_arc(r-h/4,w/2,h/2);
difference()
{
chopped_arc(r,w,h);
difference()
{
ball()chopped_arc(r-h/4,w/2,h/2);
    chopped_arc(r-h/4,w/2+e,h/2+e);
}
}
}