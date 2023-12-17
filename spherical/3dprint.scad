
use <2tri1penta_alt.scad>;

r=200;
w=12;
h=12;
e=.001;

screw_hole_d=2.5;
screw_depth=25;
screw_head_d=7;

head_off_center=w*(3/8);

module drillhole(diameter, length, head_diameter)
{
	rotate([90,0,0])
	{
	translate([0,0,-length/2])
	cylinder(length+e, r=diameter/2, center=true, $fn=20);

	translate([0,0,length/2])
	cylinder(length, r=head_diameter/2, center=true, $fn=20);
	}
}

difference()
{
	union()
	{
		chopped_arc(r-h/4,w/2,h/2);
		difference()
		{
			chopped_arc(r,w,h);
			difference()
			{
				ball() chopped_arc(r-h/4,w/2,h/2);
				chopped_arc(r-h/4-e/2,w/2+e,h/2+e);
			}
		}
	}
	ball()both_sides()
	{
		translate([r-h/2,-head_off_center,0])
		drillhole(screw_hole_d,screw_depth,screw_head_d);
	}
}
