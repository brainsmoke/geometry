points = [
[0.000000e+00,3.654880e-01],[-3.899872e-01,-2.060113e-01],[3.899872e-01,-2.060113e-01]];
vertex_holes = [
	.5,.3,.3];
edge_holes = [
	.0,.0,.0];
fn=[5,3,3];
r=[18+36,0,60];

midpoints = [ for (i=[0:len(points)-1]) (points[i]+points[(i+1)%len(points)])/2 ];

module shape()
{

	difference()
	{
		polygon( points );
		union()
		{
			for (i=[0:len(points)-1])
				translate(points[i])
rotate([0,0,r[i]])
					circle(r=vertex_holes[i], $fn=fn[i]);
			for (i=[0:len(midpoints)-1])
				translate(midpoints[i])
					circle(r=edge_holes[i], $fn=50);
		}
	}

}

module facet(s,t)
{
	translate([0,0,s])
		linear_extrude(height=t)
			scale([s,s])
				shape();
}module ball(r,t) {
multmatrix (m=[[0.000000e+00,1.000000e+00,-5.551115e-17,0.000000e+00],[1.000000e+00,0.000000e+00,0.000000e+00,0.000000e+00],[0.000000e+00,-5.551115e-17,-1.000000e+00,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-6.914901e-01,-4.467063e-01,-5.677102e-01,0.000000e+00],[-3.090170e-01,8.932643e-01,-3.264774e-01,0.000000e+00],[6.529547e-01,-5.032378e-02,-7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[8.932643e-01,-4.467063e-01,5.032378e-02,0.000000e+00],[-3.090170e-01,-6.914901e-01,-6.529547e-01,0.000000e+00],[3.264774e-01,5.677102e-01,-7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[5.520677e-01,-5.958421e-01,5.832611e-01,0.000000e+00],[-8.090170e-01,-5.520677e-01,2.017741e-01,0.000000e+00],[2.017741e-01,-5.832611e-01,-7.868251e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.273644e-01,3.167924e-01,-8.467598e-01,0.000000e+00],[8.090170e-01,-5.520677e-01,2.017741e-01,0.000000e+00],[-4.035482e-01,-7.712742e-01,-4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-9.794321e-01,-1.976240e-01,-4.071279e-02,0.000000e+00],[-2.567391e-16,2.017741e-01,-9.794321e-01,0.000000e+00],[2.017741e-01,-9.592872e-01,-1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.394225e-01,9.611227e-01,-2.383368e-01,0.000000e+00],[-5.000000e-01,-1.394225e-01,-8.547288e-01,0.000000e+00],[-8.547288e-01,2.383368e-01,4.611227e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-2.017741e-01,-1.976240e-01,9.592872e-01,0.000000e+00],[2.636780e-16,9.794321e-01,2.017741e-01,0.000000e+00],[-9.794321e-01,4.071279e-02,-1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.658998e-01,-5.658747e-01,-6.802376e-01,0.000000e+00],[-5.000000e-01,-4.658998e-01,7.300256e-01,0.000000e+00],[-7.300256e-01,6.802376e-01,-6.587468e-02,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-6.914901e-01,-6.347193e-01,3.449243e-01,0.000000e+00],[3.090170e-01,-6.914901e-01,-6.529547e-01,0.000000e+00],[6.529547e-01,-3.449243e-01,6.742977e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.658998e-01,5.658747e-01,6.802376e-01,0.000000e+00],[-5.000000e-01,-4.658998e-01,7.300256e-01,0.000000e+00],[7.300256e-01,-6.802376e-01,6.587468e-02,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[5.520677e-01,-3.167924e-01,-7.712742e-01,0.000000e+00],[8.090170e-01,4.273644e-01,4.035482e-01,0.000000e+00],[2.017741e-01,-8.467598e-01,4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-6.914901e-01,6.347193e-01,-3.449243e-01,0.000000e+00],[3.090170e-01,6.914901e-01,6.529547e-01,0.000000e+00],[6.529547e-01,3.449243e-01,-6.742977e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.658998e-01,-5.658747e-01,-6.802376e-01,0.000000e+00],[-5.000000e-01,4.658998e-01,-7.300256e-01,0.000000e+00],[7.300256e-01,6.802376e-01,-6.587468e-02,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[5.520677e-01,3.167924e-01,7.712742e-01,0.000000e+00],[8.090170e-01,-4.273644e-01,-4.035482e-01,0.000000e+00],[2.017741e-01,8.467598e-01,-4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.394225e-01,-9.611227e-01,2.383368e-01,0.000000e+00],[-5.000000e-01,1.394225e-01,8.547288e-01,0.000000e+00],[-8.547288e-01,-2.383368e-01,-4.611227e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-2.017741e-01,1.976240e-01,-9.592872e-01,0.000000e+00],[2.636780e-16,-9.794321e-01,-2.017741e-01,0.000000e+00],[-9.794321e-01,-4.071279e-02,1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.658998e-01,5.658747e-01,6.802376e-01,0.000000e+00],[-5.000000e-01,4.658998e-01,-7.300256e-01,0.000000e+00],[-7.300256e-01,-6.802376e-01,6.587468e-02,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[5.520677e-01,5.958421e-01,-5.832611e-01,0.000000e+00],[-8.090170e-01,5.520677e-01,-2.017741e-01,0.000000e+00],[2.017741e-01,5.832611e-01,7.868251e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.273644e-01,-3.167924e-01,8.467598e-01,0.000000e+00],[8.090170e-01,5.520677e-01,-2.017741e-01,0.000000e+00],[-4.035482e-01,7.712742e-01,4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-9.794321e-01,1.976240e-01,4.071279e-02,0.000000e+00],[-2.567391e-16,-2.017741e-01,9.794321e-01,0.000000e+00],[2.017741e-01,9.592872e-01,1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[0.000000e+00,-1.000000e+00,5.551115e-17,0.000000e+00],[1.000000e+00,0.000000e+00,0.000000e+00,0.000000e+00],[-0.000000e+00,5.551115e-17,1.000000e+00,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-6.914901e-01,4.467063e-01,5.677102e-01,0.000000e+00],[-3.090170e-01,-8.932643e-01,3.264774e-01,0.000000e+00],[6.529547e-01,5.032378e-02,7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[8.932643e-01,4.467063e-01,-5.032378e-02,0.000000e+00],[-3.090170e-01,6.914901e-01,6.529547e-01,0.000000e+00],[3.264774e-01,-5.677102e-01,7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.026686e-16,-9.185744e-01,-3.952481e-01,0.000000e+00],[-1.000000e+00,-7.594114e-17,-8.326673e-17,0.000000e+00],[4.647110e-17,3.952481e-01,-9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[6.914901e-01,6.347193e-01,-3.449243e-01,0.000000e+00],[3.090170e-01,-6.914901e-01,-6.529547e-01,0.000000e+00],[-6.529547e-01,3.449243e-01,-6.742977e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-8.932643e-01,3.904426e-01,2.227859e-01,0.000000e+00],[3.090170e-01,8.932643e-01,-3.264774e-01,0.000000e+00],[-3.264774e-01,-2.227859e-01,-9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-5.520677e-01,3.167924e-01,7.712742e-01,0.000000e+00],[8.090170e-01,4.273644e-01,4.035482e-01,0.000000e+00],[-2.017741e-01,8.467598e-01,-4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.273644e-01,4.368275e-02,-9.030235e-01,0.000000e+00],[-8.090170e-01,4.273644e-01,4.035482e-01,0.000000e+00],[4.035482e-01,9.030235e-01,-1.473003e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[9.794321e-01,1.976240e-01,4.071279e-02,0.000000e+00],[2.289835e-16,2.017741e-01,-9.794321e-01,0.000000e+00],[-2.017741e-01,9.592872e-01,1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-1.394225e-01,-7.886606e-01,-5.988120e-01,0.000000e+00],[5.000000e-01,4.658998e-01,-7.300256e-01,0.000000e+00],[8.547288e-01,-4.011880e-01,3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[2.017741e-01,-1.976240e-01,9.592872e-01,0.000000e+00],[-1.249001e-16,-9.794321e-01,-2.017741e-01,0.000000e+00],[9.794321e-01,4.071279e-02,-1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.658998e-01,7.886606e-01,-4.011880e-01,0.000000e+00],[5.000000e-01,1.394225e-01,8.547288e-01,0.000000e+00],[7.300256e-01,-5.988120e-01,-3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[6.914901e-01,4.467063e-01,5.677102e-01,0.000000e+00],[-3.090170e-01,8.932643e-01,-3.264774e-01,0.000000e+00],[-6.529547e-01,5.032378e-02,7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.658998e-01,-7.886606e-01,4.011880e-01,0.000000e+00],[5.000000e-01,1.394225e-01,8.547288e-01,0.000000e+00],[-7.300256e-01,5.988120e-01,3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-5.520677e-01,5.958421e-01,-5.832611e-01,0.000000e+00],[-8.090170e-01,-5.520677e-01,2.017741e-01,0.000000e+00],[-2.017741e-01,5.832611e-01,7.868251e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[6.914901e-01,-4.467063e-01,-5.677102e-01,0.000000e+00],[-3.090170e-01,-8.932643e-01,3.264774e-01,0.000000e+00],[-6.529547e-01,-5.032378e-02,-7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.658998e-01,7.886606e-01,-4.011880e-01,0.000000e+00],[5.000000e-01,-1.394225e-01,-8.547288e-01,0.000000e+00],[-7.300256e-01,-5.988120e-01,-3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-5.520677e-01,-5.958421e-01,5.832611e-01,0.000000e+00],[-8.090170e-01,5.520677e-01,-2.017741e-01,0.000000e+00],[-2.017741e-01,-5.832611e-01,-7.868251e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-1.394225e-01,7.886606e-01,5.988120e-01,0.000000e+00],[5.000000e-01,-4.658998e-01,7.300256e-01,0.000000e+00],[8.547288e-01,4.011880e-01,-3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[2.017741e-01,1.976240e-01,-9.592872e-01,0.000000e+00],[-1.249001e-16,9.794321e-01,2.017741e-01,0.000000e+00],[9.794321e-01,-4.071279e-02,1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.658998e-01,-7.886606e-01,4.011880e-01,0.000000e+00],[5.000000e-01,-1.394225e-01,-8.547288e-01,0.000000e+00],[7.300256e-01,5.988120e-01,3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-5.520677e-01,-3.167924e-01,-7.712742e-01,0.000000e+00],[8.090170e-01,-4.273644e-01,-4.035482e-01,0.000000e+00],[-2.017741e-01,-8.467598e-01,4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.273644e-01,-4.368275e-02,9.030235e-01,0.000000e+00],[-8.090170e-01,-4.273644e-01,-4.035482e-01,0.000000e+00],[4.035482e-01,-9.030235e-01,1.473003e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[9.794321e-01,-1.976240e-01,-4.071279e-02,0.000000e+00],[2.289835e-16,-2.017741e-01,9.794321e-01,0.000000e+00],[-2.017741e-01,-9.592872e-01,-1.976240e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.026686e-16,9.185744e-01,3.952481e-01,0.000000e+00],[-1.000000e+00,7.594114e-17,8.326673e-17,0.000000e+00],[4.647110e-17,-3.952481e-01,9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[6.914901e-01,-6.347193e-01,3.449243e-01,0.000000e+00],[3.090170e-01,6.914901e-01,6.529547e-01,0.000000e+00],[-6.529547e-01,-3.449243e-01,6.742977e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-8.932643e-01,-3.904426e-01,-2.227859e-01,0.000000e+00],[3.090170e-01,-8.932643e-01,3.264774e-01,0.000000e+00],[-3.264774e-01,2.227859e-01,9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[8.932643e-01,3.904426e-01,2.227859e-01,0.000000e+00],[3.090170e-01,-8.932643e-01,3.264774e-01,0.000000e+00],[3.264774e-01,-2.227859e-01,-9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.273644e-01,3.167924e-01,-8.467598e-01,0.000000e+00],[8.090170e-01,5.520677e-01,-2.017741e-01,0.000000e+00],[4.035482e-01,-7.712742e-01,-4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-1.394225e-01,-9.611227e-01,2.383368e-01,0.000000e+00],[-5.000000e-01,-1.394225e-01,-8.547288e-01,0.000000e+00],[8.547288e-01,-2.383368e-01,-4.611227e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-8.932643e-01,4.467063e-01,-5.032378e-02,0.000000e+00],[-3.090170e-01,-6.914901e-01,-6.529547e-01,0.000000e+00],[-3.264774e-01,-5.677102e-01,7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.273644e-01,-4.368275e-02,9.030235e-01,0.000000e+00],[-8.090170e-01,4.273644e-01,4.035482e-01,0.000000e+00],[-4.035482e-01,-9.030235e-01,1.473003e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.394225e-01,-7.886606e-01,-5.988120e-01,0.000000e+00],[5.000000e-01,-4.658998e-01,7.300256e-01,0.000000e+00],[-8.547288e-01,-4.011880e-01,3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-8.932643e-01,-4.467063e-01,5.032378e-02,0.000000e+00],[-3.090170e-01,6.914901e-01,6.529547e-01,0.000000e+00],[-3.264774e-01,5.677102e-01,-7.557233e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[4.273644e-01,4.368275e-02,-9.030235e-01,0.000000e+00],[-8.090170e-01,-4.273644e-01,-4.035482e-01,0.000000e+00],[-4.035482e-01,9.030235e-01,-1.473003e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[1.394225e-01,7.886606e-01,5.988120e-01,0.000000e+00],[5.000000e-01,4.658998e-01,-7.300256e-01,0.000000e+00],[-8.547288e-01,4.011880e-01,-3.293734e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[8.932643e-01,-3.904426e-01,-2.227859e-01,0.000000e+00],[3.090170e-01,8.932643e-01,-3.264774e-01,0.000000e+00],[3.264774e-01,2.227859e-01,9.185744e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-4.273644e-01,-3.167924e-01,8.467598e-01,0.000000e+00],[8.090170e-01,-5.520677e-01,2.017741e-01,0.000000e+00],[4.035482e-01,7.712742e-01,4.922245e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
multmatrix (m=[[-1.394225e-01,9.611227e-01,-2.383368e-01,0.000000e+00],[-5.000000e-01,1.394225e-01,8.547288e-01,0.000000e+00],[8.547288e-01,2.383368e-01,4.611227e-01,0.000000e+00],[0, 0, 0, 1]]) {facet(r,t);};
}
ball(200, .8);
