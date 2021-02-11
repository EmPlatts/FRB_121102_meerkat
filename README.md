### Find structure optimised dispersion measure (DM) for FRB 121102
 Find structure optimised DM for FRBs using autocorrelation functions (ACFs), as described in [Lange (1998)](http://articles.adsabs.harvard.edu/pdf/1998A%26A...332..111L). Code used in Platts, Caleb, Stappers, Main, Weltman, Shock et al. (in prep).
 
 Archives are processed with [PSRCHIVE](http://psrchive.sourceforge.net/) and [SIGPROC](https://github.com/SixByNine/sigproc). Data saved to text files for each DM in search range using:
 
      pdv -F -t -jD <filename>.ar > <filename>.txt
 
 To run the ACF code:
      
      python ACF_Lange.py -s txt -o1 <on_pulse> -o2 <off_pulse> -t <step>
      
 where <on_pulse> and <off_pulse> are the bins of the pulse region and <step> is the step size of between bins.

 After which, run `find_opt_dm.py`. Read code and adjust parameters as needed.
 
 ### Please Note:
 Unfortunately, this code is not a plug-and-play. You will need to find the sensitivity parameters c1 and c2 that suit your pulses. In general, ACFs that have a more clear flattening point have c1=2 and c2=0.5 (first image), and ACFs with a less clear flattening point have higher values (e.g. for our sample of pulses, c1=4 and c2=4; second image).
 
 <img src="https://github.com/EmPlatts/FRB_121102_meerkat/blob/main/img/ACF_example.png" width="500">  <img src="https://github.com/EmPlatts/FRB_121102_meerkat/blob/main/img/ACF_compare.png" width="500">
 
 Additionally, noise in the ACF may influence the algorithm, and the points may get "stuck" on noise spikes. For example, in the image below, the red points are incorrectly identified as flattening points if the sensitivity parameters are too high. The green point shows the correct flattening point.
 
 <img src="https://github.com/EmPlatts/FRB_121102_meerkat/blob/main/img/Lange_ACF.png" width="500">
 
 Finally, you will need to set the smoothing factor for spline.
 
