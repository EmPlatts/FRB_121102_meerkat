### Find structure optimised dispersion measure (DM) for FRB 121102
 Find structure optimised DM for FRBs using autocorrelation functions. Code used in Platts, Caleb, Stappers et al. (2020).
 Not recommended for general use. Only tested on 10 pulses.
 
 Archives are processed with [PSRCHIVE](http://psrchive.sourceforge.net/) and [SIGPROC](https://github.com/SixByNine/sigproc). Data saved to text files for each DM in search range using:
 
      pdv -F -t -jD <filename>.ar > <filename>.txt
 
 To run the ACF code:
      
      python ACF_Lange.py -s txt -o1 <on_pulse> -o2 <off_pulse> -t <step>
      
 where <on_pulse> and <off_pulse> are the bins of the pulse region and <step> is the step size of between bins.

 After which, run `find_opt_dm.py`. Read code and adjust parameters as needed.
 
 
