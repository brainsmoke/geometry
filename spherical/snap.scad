
module hook_profile(w, d, stroke, notch_r, notch_y, base_d)
{
	e=.00001;
	$fn=16;

	translate([-w/2, 0])
		square([stroke, d-stroke/2]);

	hull()
	{
		for (p = [
			[-w/2+stroke/2, d-stroke/2],
			[w/2-stroke/2, notch_y],
		])
			translate(p)
				circle(stroke/2);
	}

	translate([-w/2, notch_y])
		circle(notch_r);

	hull()
	{
		translate([-w/2+stroke/2, notch_y])
			circle(stroke/2);
		translate([-w/2, -base_d])
			square([w/2, base_d]);
	}

	translate([-w/2, -base_d])
		square([w, base_d]);
	
}

module latch_profile(w, d, stroke, notch_r, notch_y, base_d, v_margin)
{
	$fn=16;

	translate([-w/2, notch_y])
		circle(notch_r+v_margin);

	translate([-w/2-v_margin, -base_d+v_margin])
		square([w+2*v_margin, base_d+d]);
}


module hook(h, w, d, stroke, notch_r, notch_y, base_d)
{
	linear_extrude(h)
		hook_profile(w, d, stroke, notch_r, notch_y, base_d);
}

module latch(h, w, d, stroke, notch_r, notch_y, base_d, v_margin, h_margin)
{
	translate([0,0,-h_margin])
		linear_extrude(h+h_margin*2)
			latch_profile(w, d, stroke, notch_r, notch_y, base_d, v_margin);
}

module snap_test()
{

	for (x = [0, 20])
		translate([x,0,0]) 
		{
			translate([-4,-8,0])
				cube([8,8,8]);
			hook(8, 4, 5, 1, .75, 2, 3);
		}

	translate([30,0,0])
		difference()
		{
			cube([8, 30, 8]);
			union()
			{
				translate([4,12,0])
					rotate([90,0,0])
						latch(8, 4, 5, 1, .75, 2, 3, .2, .2);

				translate([4,16,8])
					rotate([-90,0,0])
						latch(8, 4, 5, 1, .75, 2, 3, .2, .2);
			}
	}
}

snap_test();
