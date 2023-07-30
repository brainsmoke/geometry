#!/usr/bin/env python3

import sys, cmath

import kit

kind = (sys.argv[1:] + ['penta'])[0]
assert kind in ('penta', 'tri')
r = 250 # outer radius, measured at the midpoint of the facet
width = 18
height = 18
subdivisions=2
notch_width = 3

thickness=3

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_width)

tubearc = """

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


"""

generator = {
    'penta':"""
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
""",
    'tri':"""
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
"""
}

def shape_module(name, points):
    print (f"module {name}"+""" ()
{
	linear_extrude(thickness) polygon(["""+','.join(f"[{x}, {y}]" for x,y in points)+"""]);
}""")

def tube(shapes, kind, r, width, height, subdivisions, thickness):
    print(f"""
r = {r};
w = {width};
h = {height};
subdivisions = {subdivisions};
thickness = {thickness};

""")
    print(tubearc)
    print(generator[kind])

    shape_module("top_joint", shapes[0])
    shape_module("bottom_joint", shapes[1])
    arc_ix = 2
    top_div = []
    bottom_div = []
    if subdivisions > 1:
        arc_ix=4
        top_div = shapes[2]
        bottom_div = shapes[3]
    shape_module("top_div", top_div)
    shape_module("bottom_div", bottom_div)

    shape_module("big_arc", shapes[arc_ix])
    shape_module("small_arc", shapes[arc_ix+1])

    print(f"{kind}()extend()arc();")

