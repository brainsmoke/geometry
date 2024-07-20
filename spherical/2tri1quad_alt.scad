$fn=100;
e=.001;

r=100;
w=8;
h=6;

/*
 * alpha: the regular spherical triangles' great-circle arc (edge-length)
 * beta:  the regular spherical squares' great-circle arc (edge-length)
 *
 * A: the triangles' corner arc
 * B: the squares' corner arc
 * A+B = tau/2
 *
 * alpha = 2*beta
 * cos (alpha) = 1 / (1-cos(A)) - 1
 * cos (beta)  = 2 / (1-cos(B)) - 1
 * cos (beta)  = 2 / (1+cos(A)) - 1
 *
 * let x = cos(A)
 *
 * 1 / (1-x) -1 = 2 * ( 2/(1+x) - 1 )^2 - 1
 *
 */

cuberoot=pow(24*sqrt(78)-181, 1/3);
cos_A=(1/6)*(5) -
      (1/6)*(23)/cuberoot +
      (1/6)*cuberoot;

A=acos(cos_A);

cos_alpha=1/(1-cos_A)-1;
alpha=acos(cos_alpha);

include <arcs.scad>

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

module quad()
{
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

module extend()
{
    children();
    step_y()step_x(){
        children();
        step_x(){
            children();
        }
    }
}

module ball()
{
    quad()extend()children();
}

ball()chopped_arc(r,w,h);
