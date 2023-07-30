module subdiv_arc(a, n)
{
    if (n > 0)
        rotate([0,0,a])
        {
            children();
            subdiv_arc(a,n-1)children();
        }
}

module joint()
{
    translate([r-thickness,0,0])
    rotate([0,90,0])
    rotate([0,0,90-A])
    top_joint();
    
    translate([r-h+thickness,0,0])
    rotate([0,-90,0])
    rotate([0,0,A-90])
    bottom_joint();
}

module subdiv()
{
    translate([r-thickness,0,0])
    rotate([0,90,0])
    rotate([0,0,90])
    top_div();
    
    translate([r-h+thickness,0,0])
    rotate([0,-90,0])
    rotate([0,0,90])
    bottom_div();
}

module big_side()
{
    translate([r,(w/2)*(cos_A+1)/sin(A),-w/2])
    rotate([0,0,90])
    big_arc();
}

module small_side()
{
    translate([r,-(w/2)*(cos_A-1)/sin(A),w/2])
    rotate([180-A,0,0])
    rotate([0,0,90])
    small_arc();
}

module arc()
{
    joint();
    
    subdiv_arc(alpha/2/subdivisions, subdivisions-1)subdiv();

    rotate([-A,0,0])
    subdiv_arc(alpha/2/subdivisions, subdivisions-1)subdiv();
    
    big_side();
    small_side();
}

