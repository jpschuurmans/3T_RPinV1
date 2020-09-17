#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 20:01:55 2020

@author: petras
"""

# This script will generate each subjects design.fsf, but does not run it.

# It depends on your system how will launch feat
import os
import re
import glob

 

# set to dir that contains all subject dirs

studydir = '//media/petras/DATA/iCOARSE/MRI_data/'
 

# Set this to directory with all the fsf files

# May want to make it a separate directory, because you can delete them all o

#   once Feat runs

fsfdir="%sFSL/feat_files/"%(studydir)

 

# Get all the paths. glob.glob is like a loop but doesn't break when not all
#subs have the same number of runs

subdirs=glob.glob("%s//sub[0-9]*/ses-[0-9]*/sub-[0-9]*_ses-[0-9]*_"
                  "task-iCoarse_acq-EP3D_dir-RL_run-[1-9]*_mag_MoCorr_DistCorr_Study.nii.gz"%(studydir))

for dir in list(subdirs):
    #find the regular expression of a number following the string "sub" in dir
  #the [0] is just to take only the first entry in case there are more than 1
  subnum = str(re.findall(r'%s(\d+)' %"sub", dir)[0])
  #same trick  for the session
  sessnum = str(re.findall(r'%s(\d+)' %"ses-", dir)[0])
  #and the same for the run
  runnum= str(re.findall(r'%s(\d+)' %"run-", dir)[0])

  ntime = os.popen('fslnvols %s' %(dir)).read().rstrip()

  replacements = {'SUBNUM':subnum, 'NTPTS':ntime,'SESSNUM':sessnum, 'RUNNUM':runnum}

  with open("%s/template_lev1.fsf"%(fsfdir)) as infile:

    with open("%s/lev1/design_sub%s_session%s_run%s.fsf"%(fsfdir, subnum, sessnum, runnum), 'w') as outfile:

        for line in infile:

          for src, target in replacements.items():

            line = line.replace(src, target)

          outfile.write(line)
          
 # os.system("feat %s/lev1/design_sub%s_sess%s_run%s.fsf"%(fsfdir, subnum, sessnum, runnum))
