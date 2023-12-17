
use <2tri1penta_alt.scad>;

r=200;
w=12;
h=12;
e=.001;

joint_spacing=.5; /* positive -> more space, negative -> friction fit */
joint_h = h/2;
joint_w = w/2;

hole_h = joint_h+joint_spacing;
hole_w = joint_w+joint_spacing;

screw_hole_d=2.5;
screw_depth=25;
screw_head_d=7;

head_off_center=w*(3/8);

module drill_hole(diameter, length, head_diameter)
{
	rotate([90,0,0])
	{
	translate([0,0,-length/2])
	cylinder(length+e, r=diameter/2, center=true, $fn=20);

	translate([0,0,length/2])
	cylinder(length, r=head_diameter/2, center=true, $fn=20);
	}
}

module drill_holes()
{
	ball()both_sides()
	{
		translate([r-h/2,-head_off_center,0])
		drill_hole(screw_hole_d,screw_depth,screw_head_d);
	}
}

module joint_holes()
{
	difference()
	{
		ball() chopped_arc(r-(hole_h)/2,hole_w,hole_h);
		chopped_arc(r-(hole_h-e)/2, hole_w+e, hole_h+e);
	}
}

difference()
{
	union()
	{
		chopped_arc(r-joint_h/2,joint_w,joint_h);
		difference()
		{
			chopped_arc(r,w,h);
			joint_holes();
		}
	}
	drill_holes();
}
