
module arc(r, w, h)
{
    rotate_extrude(angle=alpha*3/2)
    translate([r-h/2,0])square([h,w],center=true);
}

module both_sides()
{
        for (i = [[0,0], [alpha*3/2,180]])
        rotate([0,0,i[0]])
        rotate([i[1],0,0])
		children();
}

module chopped(r,w,h)
{
		both_sides()
        rotate([A,0,0])
        translate([r,0,0])
        cube([2*(w+h),2*(w+h),w-e],center=true);
}

module chopped_arc(r,w,h)
{
    difference()
    {
        arc(r,w,h);
        chopped(r,w,h);
    }
}

module spherical_arc(r,w,h)
{
    intersection()
    {
        chopped_arc(r+h,w,h+r);
        difference()
        {
            sphere(r);
            sphere(r-h);
        }
    }
}

