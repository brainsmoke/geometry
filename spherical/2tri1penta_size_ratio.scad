$fn=100;
e=.001;

r=100;
w=6;
h=6;
size_ratio_triangle = 2;
size_ratio_pentagon = 1;


n_triangles = 20;
n_pentagons = 12;

ratio_triangles = n_triangles*size_ratio_triangle /
                ( n_triangles*size_ratio_triangle +
                  n_pentagons*size_ratio_pentagon );

ratio_pentagons = 1-ratio_triangles;

/* openscad does trig in degrees :-/ */
solid_angle_total = 720;

solid_angle_per_triangle = solid_angle_total*ratio_triangles/n_triangles;

solid_angle_per_pentagon = solid_angle_total*ratio_pentagons/n_pentagons;

excess_angle_triangle = solid_angle_per_triangle/3;
excess_angle_pentagon = solid_angle_per_pentagon/5;

/*
 * alpha: the regular spherical triangles' great-circle arc (edge-length)
 * beta:  the regular spherical pentagons' great-circle arc (edge-length)
 *
 * A: the triangles' corner arc
 * B: the pentagons' corner arc
 * A+B = tau/2
 */
A = 180 - 360/3 + excess_angle_triangle;
B = 180 - 360/5 + excess_angle_pentagon;

phi = (1+sqrt(5))/2;
alpha = acos ( 1 / (1-cos(A)) - 1 );
beta  = acos( (phi + 1) / (1-cos(B)) - 1 );

echo (A+B,alpha,beta);

module arc(r, w, h)
{
    rotate_extrude(angle=alpha+beta)
    translate([r-h/2,0])square([h,w],center=true);
}

module both_sides()
{
        for (i = [[0,0], [alpha+beta,180]])
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


module step_x()
{
    rotate([0,0,beta])rotate([-A,0,0])
    children();
}

module step_y()
{
    rotate([0,0,alpha+beta])rotate([180,0,0])
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
    step_y()step_x(){
        children();
        step_x(){
            children();
            step_x(){
                children();
                step_y()step_x(){
                    children();
                    step_y()step_x()step_x()step_x()step_x(){
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

ball()chopped_arc(r,w,h);
