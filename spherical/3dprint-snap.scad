
use <2tri1tri_alt.scad>;
//use <2tri1quad_alt.scad>;
//use <2tri1penta_alt.scad>;

r=75;
w=8;
h=8;
e=.001;

hook_width = 4;
hook_depth = 4.5;
hook_min_width = 1;
notch_radius = .75;
notch_ypos = 1.5;
margin_v = .2;
margin_h = .2;

use <snap.scad>;

module shape()
{
    base_angle = min(corner_angle(),180-corner_angle());
    base_depth = w*(1/sin(base_angle)-1/tan(base_angle));
	difference()
	{
		union()
		{
			both_sides()
				translate([r-h/2,base_depth/2,-w/2])
					rotate([0,0,180])
						hook(h, hook_width, hook_depth, hook_min_width,
						     notch_radius, notch_ypos,
						     base_depth+e);
			chopped_arc(r,w,h);
		}

		both_sides()
			step_x()
				translate([r-h/2,base_depth/2,-w/2])
					rotate([0,0,180])
						latch(h, hook_width, hook_depth, hook_min_width,
						      notch_radius, notch_ypos,
							  base_depth+e, margin_v, margin_h);
}
}


module test()
{
	difference()
	{
		shape();
		union()
		{
			for (i=[1,3,5])
				rotate([0,0,i/6*arc_angle()])
					translate([75,0,0])
						cube([40,40,40], center=true);
		}
	}
}


//ball()
shape();

