# DJR_plotting
Make differential jet rate plots from miniAOD samples on FNAL's condor
```
python runJobs.py
hadd sample.root [sample]/hists*root
root 'collect.C("sample.root","plots.root")' 
```

