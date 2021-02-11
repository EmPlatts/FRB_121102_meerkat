import numpy as np
from scipy import interpolate
import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt

pulse_name = '09' 

iffts = np.load('output_data/iffts_'+pulse_name+'.npy')
time_lag = np.load('output_data/time_lag_'+pulse_name+'.npy')

# Adjust to region of interest
min_dm_idx = 5620-5499 #5499 is to correct for DM which starts at 550.1. Check the index for your .txt files and change as needed.
max_dm_idx = 5670-5499

time_lags = []
for i in range(min_dm_idx,max_dm_idx,1):
    iffts_file = iffts[i]
    # plt.plot(time_lag,iffts_file,label=str((i+5499)/10),linewidth=1) 
    n0 = 2 #start from second timestep to remove noise
    num_iter = 100
    c_1 = 4 #may be 2 to 4. For very curvy ACFs, c1=2, for less curvy ACFs (less defined flattening points) c1=4. Lange uses 2 for their sample.
    c_2 = 4 #may be 1.5 to 4. For very curvy ACFs, c1=1.5 or 2. Lange uses 1.5 for their sample.
    for i in range(num_iter):
        d_i = []
        d0 = np.abs(iffts_file[n0]-iffts_file[n0-1])
        # local check for 4 bins
        for i in range(n0+1,n0+5):
            d = np.abs(iffts_file[i]-iffts_file[i-1])
            d_i = np.append(d_i,d)
        if len(np.where(d_i<d0/c_1)[0]) == 0:
            n0 += 1
            continue
        # global check over 8 bins (Lange 1998 uses 4 bins - you may need to change this.)
        elif (len(np.where(d_i<d0/c_1)[0]) > 0) and (np.abs(iffts_file[n0]-iffts_file[n0-8]) < np.abs(c_2*(iffts_file[n0+8]-iffts_file[n0]))):
            n0 += 1
            continue
        elif (len(np.where(d_i<d0/c_1)[0]) > 0) and (np.abs(iffts_file[n0]-iffts_file[n0-8]) > np.abs(c_2*(iffts_file[n0+8]-iffts_file[n0]))):
            n0 += np.where(d_i<d0/c_1)[0][0] 
            break
        else:
            raise ArithmeticError('Something is amiss... Have you changed the elif statements?')

    time_lags.append(time_lag[n0])
    # plt.scatter(time_lag[n0],iffts_file[n0])
# plt.show()

# Check things look okay from choice of c_1 and c_2, and range of interest
t = time_lags
DM = (np.arange(min_dm_idx,min_dm_idx+len(t))+5499)/10
plt.xlabel(r'DM (pc cm$^{-3}$)',fontsize=12)
plt.ylabel(r'Time Lag (ms)',fontsize=12)
plt.legend(fontsize=12,loc=1)
plt.scatter(DM,t,c='k',s=1)
plt.show()

def interp_for_max_or_min(x, y, spline_smoothing_factor, spline_order=4, spline_x_step=10**3):
    spl = interpolate.UnivariateSpline(x,y,k=spline_order)    
    xs = np.linspace(min(x),max(x),spline_x_step)
    spl.set_smoothing_factor(spline_smoothing_factor)
    opt_xs = spl.derivative().roots() #find maxima and minima
    opt_ys = spl(opt_xs)
    min_index= np.argmin(opt_ys) #get minimum
    opt_x, opt_y = opt_xs[min_index], opt_ys[min_index]
    return xs, spl(xs), opt_x, opt_y, spl.derivative()

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

smoothing_factor = 10 #set smoothing factor for spline
DMs, ts, opt_DM, opt_t, deriv_fn = interp_for_max_or_min(x=DM, y=t, spline_smoothing_factor=smoothing_factor)

d_ts = deriv_fn(ts) # first deriv
dd_ts = np.gradient(d_ts) # second deriv

#Find residuals
DM_res_idx = list(map(lambda x: find_nearest(DMs,x), DM)) #index of DM in DMs corresponding to position of DM
DM_res = DMs[DM_res_idx]
t_res = ts[DM_res_idx]
residuals_ = t-t_res

# Find from std dev from Taylor expansion 1/2 y''(x_opt)(dx)^2
dd_ts_idx = find_nearest(DMs,opt_DM)
std_DM = np.sqrt(np.abs(2*np.std(residuals_)/dd_ts[dd_ts_idx]))

print('DM =',opt_DM,'+-',std_DM)

# Check output
plt.plot(DMs, ts, color='k', linewidth=1)
plt.plot(DM, t, color='k', linewidth=0.5,linestyle='--')
plt.scatter(opt_DM, opt_t, s=10, c='k', label='DM = '+str(round(opt_DM,1))+r'$\pm$'+str(round(std_DM,1)))
plt.xlabel(r'DM (pc cm$^{-3}$)',fontsize=12)
plt.ylabel(r'Time Lag (ms)',fontsize=12)
plt.legend(fontsize=12,loc=1)
plt.tight_layout()
plt.savefig('output_plots/timelag_DM_'+pulse_name+'.png', dpi=300)
plt.show()
