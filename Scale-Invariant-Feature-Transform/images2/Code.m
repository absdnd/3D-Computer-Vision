I = rgb2gray(imread('images2/5_1.jpg'));
J = rgb2gray(imread('images2/5_2.jpg'));
I1 = imresize(I,0.2);
I2 = imresize(J,0.2);
l=[481 237;
462 241;
468 286;
474 253;
274 55;
264 65;
280 70;
255 48;
281 259;
143 109;
470 125;
49 111;
44 134;
313 190;
458 373;
309 410;
380 461;
385 442];

s=[198 225;
   179 227;
   155 217;
   192 240;
   492 42;
   497 57;
   488 65;
   498 72;
   479 51;
   414 230;
   413 129;
   304 94;
   325 100;
   542 116;
   237 369;
   420 359;
   413 427;
   433 468]


figure; ax = axes;
showMatchedFeatures(I2,I1,l,s,'montage','Parent',ax);
title(ax, 'Candidate point matches');
legend(ax, 'Matched points 1','Matched points 2');
