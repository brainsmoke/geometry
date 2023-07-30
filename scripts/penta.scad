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

