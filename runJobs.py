import os

#first
#dasgoclient -query="file dataset=/DYJetsToLL_Pt-50To100_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM" > DYJetsToLL_Pt-50To100_TuneCP5_13TeV-amcatnloFXFX-pythia8.txt

#sample="/DYJetsToLL_Pt-50To100_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM"
#sample="/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM" #LO incl
sample="/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM" #NLO incl
name = sample.split("/")[1]

try:
    os.mkdir(name)
except:
    pass
os.chdir(name)
os.system("ln -s ../batchplotdjr.C .")
command = 'dasgoclient -query="file dataset={}" > {}'.format(sample,name+".txt")
print(command)
os.system(command)


condor_runscript = """#!/bin/bash
export ORIG_DIR=$PWD
cd /cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_6_0/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
cd $ORIG_DIR


xrdcp root://cmsxrootd.fnal.gov/$1 .
export LOCALFILENAME=`basename "$1"`


root -b "batchplotdjr.C(\\"$LOCALFILENAME\\")";
rm $LOCALFILENAME;
"""

#+RequestMemory=4000
submit_file = """
universe = vanilla
Executable = condor_runscript.sh
Should_Transfer_Files = YES
transfer_input_files=batchplotdjr.C
Notification = never
Output = log-$(ClusterId).$(ProcId).stdout
Error  = log-$(ClusterId).$(ProcId).stderr
Log    = log-$(ClusterId).$(ProcId).log

+MaxRuntime = 4*60*60
Queue Arguments from (
"""
with open(name+".txt","r") as f:
    for line in f:
        submit_file+=line
    submit_file+=")\n"

with open("submit.sub","w") as sub:
    sub.write(submit_file)

with open("condor_runscript.sh","w") as runscr:
    runscr.write(condor_runscript)
