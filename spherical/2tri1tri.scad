$fn=100;
e=.001;

r=100;
w=1;
h=20;

/*
 * alpha = 2*beta
 * cos (alpha) = 1 / (1-cos(A)) - 1
 * cos (beta)  = 1 / (1+cos(A)) - 1
 *
 * let x = cos(A)
 *
 * 1 / (1-x) -1 = 2 * ( 1/(1+x) - 1 )^2 - 1
 *
 * 2x^3 - x^2 + 2x + 1 = 0
 */

cuberoot=pow(6*sqrt(177)-71,1/3);
cos_A=(1/6)*(1) -
      (1/6)*(11)/cuberoot +
      (1/6)*cuberoot;
A=acos(cos_A);

cos_alpha=1/(1-cos_A)-1;
alpha=acos(cos_alpha);

echo (A, alpha*3/2);

module arc(r, w, h)
{
    rotate_extrude(angle=alpha*3/4)
    translate([r-h/2,0])square([h,w],center=true);
}

module chopped_arc(r,w,h)
{
    difference(){
        arc(r,w,h);

        rotate([-A,0,0])
        translate([r,0,0])
        cube([w+h,w+h,w-e],center=true);
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

module step_x()
{
    rotate([0,0,alpha/2])rotate([A,0,0])
    children();
}

module step_y()
{
    rotate([0,0,3*alpha/2])rotate([180,0,0])
    children();
}

module tri()
{
    children();
    step_x(){
        children();
        step_x(){
            children();
        }
    }
}

module extend()
{
    children();
    step_y()tri()children();
}

module ball()
{
    tri()extend()children();
}

module smooth_ball_alt(r,w,h)
{
    intersection()
    {
        ball()arc(r+h,w,h+r);
        difference()
        {
            sphere(r);
            sphere(r-h);
        }
    }
}

ball()chopped_arc(r,w,h);

//ball()spherical_arc(r,w,h); /* slow */

//smooth_ball_alt(r,w,h); /* slow */
