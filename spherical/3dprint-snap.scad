
use <2tri1tri_alt.scad>;
//use <2tri1quad_alt.scad>;
//use <2tri1penta_alt.scad>;

r=75;
w=8;
h=8;
e=.001;

min_border_thickness_xy = 0.5;
min_border_thickness_z = 0.5;

hook_width = 4;
hook_depth = 4.5;
hook_min_width = 1;
notch_radius = .75;
notch_ypos = 1.5;
margin_v = .2;
margin_h = .2;

use <snap.scad>;

base_angle = min(corner_angle(),180-corner_angle());
hook_offset = (w/2)*(1/sin(base_angle)-1/tan(base_angle));
base_depth = w/tan(base_angle);

max_latch_radius = sqrt( pow(r-w/2+hook_width/2+notch_radius+margin_v, 2) +
                         pow((w/2+margin_h)*sin(base_angle), 2));

max_hook_depth = sin(base_angle)*(base_depth + hook_depth + margin_h)+margin_v*cos(base_angle);

echo ("min border width (arc) = ", r-max_latch_radius);
assert(r-max_latch_radius >= min_border_thickness_xy);

echo ("min border width (top/bottom) = ", w-max_hook_depth);
assert(w-max_hook_depth >= min_border_thickness_z);

module shape()
{
	difference()
	{
		union()
		{
			both_sides()
				translate([r-h/2,hook_offset,-w/2])
					rotate([0,0,180])
						hook(h, hook_width, hook_depth, hook_min_width,
						     notch_radius, notch_ypos,
						     base_depth+e);
			chopped_arc(r,w,h);
		}

		both_sides()
			step_x()
				translate([r-h/2,hook_offset,-w/2])
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

