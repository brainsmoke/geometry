
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

