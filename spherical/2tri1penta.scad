$fn=100;
e=.001;

r=100;
w=8;
h=6;

/*
 * alpha = 2*beta
 * cos (alpha) = 1 / (1-cos(A)) - 1
 * cos (beta)  = (phi + 1) / (1+cos(A)) - 1
 *
 * let x = cos(A)
 *
 * 1 / (1-x) -1 = 2 * ( (phi + 1)/(1+x) - 1 )^2 - 1
 *
 * x^3+(-2*phi-1/2)x^2+(3*phi+2)x + (-phi-1/2) = 0
 */

phi=(1+sqrt(5))/2;
cuberoot=pow(118*phi+85+6*sqrt(1173*phi+729), 1/3);
cos_A=(1/6)*(4*phi+1) +
      (1/6)*(12*phi+7)/cuberoot -
      (1/6)*cuberoot;

A=acos(cos_A);

cos_alpha=1/(1-cos_A)-1;
alpha=acos(cos_alpha);

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

module penta()
{
    children();
    step_x(){
        children();
        step_x(){
            children();
            step_x(){
                children();
                step_x(){
                    children();
                }
            }
        }
    }
}

module extend()
{
    children();
    step_y()step_x()step_x()step_x()
    {
        penta()children();
        step_y(){
            penta()children();
            step_x()step_x()step_y()children();
        }
    }
}

module ball(r,w,h)
{
    penta()extend()chopped_arc(r,w,h);
}

module smooth_ball(r,w,h)
{
    penta()extend()spherical_arc(r,w,h);
}

module smooth_ball_alt(r,w,h)
{
    intersection()
    {
        penta()extend()arc(r+h,w,h+r);
        difference()
        {
            sphere(r);
            sphere(r-h);
        }
    }
}

//smooth_ball(r,w,h); /* slow */
//smooth_ball_alt(r,w,h); /* slow */
ball(r,w,h);
