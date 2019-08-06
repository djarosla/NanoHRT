# NanoHRT

### Set up CMSSW

## 2016 version
```bash
cmsrel CMSSW_9_4_12
cd CMSSW_9_4_12/src
cmsenv
```

### Get customized NanoAOD producers for HeavyResTagging

```bash
git clone https://github.com/djarosla/NanoHRT.git PhysicsTools/NanoHRT
cd PhysicsTools/NanoHRT
git fetch 
git checkout origin/ForTraining --track
```

### Compile

```bash
scram b -j 16
```


MC:
```bash
cmsRun test_nanoHRT_mc_102X_NANO.py Settype=YYY
```

where YYY is the signal type - top, pho, ww, etc
