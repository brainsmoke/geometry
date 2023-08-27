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
    rotate_extrude(angle=alpha*3/2)
    translate([r-h/2,0])square([h,w],center=true);
}

module chopped(r,w,h)
{
        for (i = [0, alpha*3/2])
        rotate([0,0,i])
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

module wiring(r, w, h)
{
    difference()
    {
        union()
        {
        color([1,0,0])rotate_extrude(angle=alpha*3/2)
            translate([r-h/2,-w/3])square([h,w/10],center=true);
        color([1,1,1])rotate_extrude(angle=alpha*3/2)
            translate([r-h/2,0])square([h,w/10],center=true);
        color([0,0,0])rotate_extrude(angle=alpha*3/2)
            translate([r-h/2,w/3])square([h,w/10],center=true);
        }
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

module arrow(l, w, h)
{
    translate([0,l/2,0])cube([h,l,w],center=true);
    translate([0,l,0])rotate([90,0,90])cylinder(h,w*2,w*2,center=true,$fn=3);
}

module step_x()
{
    rotate([0,0,alpha/2])rotate([-A,0,0])
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
    $count=is_undef($count)?0:$count;
    children();
    step_y()step_x(){
        $count=$count+1;
        children();
        step_x(){
            $count=$count+1;
            children();
            step_x(){
                $count=$count+1;
                children();
                step_y()step_x(){
                    $count=$count+1;
                    children();
                    step_y()step_x()step_x()step_x()step_x(){
                        $count=$count+1; 
                        children();
                    }
                }
            }        
        }
    }
}

module ball()
{
    penta()extend()children();
}

ball(){
    color([.8,.8,.8])chopped_arc(r,w,h);
    wiring(r+1+w/10,w,w/10);
}

extend()
{
    chopped_arc(r+1,w,1);
    color([0,1,0])translate([r+4,5,0])arrow(10,w/3,3);
    color([0,0,.8])translate([r+10,-8,-w*.6])rotate([90,0,90])text(str($count));
}

