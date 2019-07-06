from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

curset = "/JetHT/Run2017D-31Mar2018-v1/MINIAOD" 
outloc = "/store/user/knash" 
version = "8" 
store = "T2_CH_CERN" 

substr = curset.split('/')[1]
substr1 = curset.split('/')[2]
print substr,substr1

ver ='_v'+version

config.section_('General')
config.General.requestName = substr+substr1+'NanoSlimNtuples'+ver
config.General.workArea = 'crab_projects'
config.General.transferLogs = False
config.General.transferOutputs = True
config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NanoAOD_Slim_data2017_NANO10_2_15.py'
config.JobType.numCores = 4
config.JobType.sendExternalFolder = True
config.JobType.maxMemoryMB = 5000
config.JobType.allowUndistributedCMSSW = True
config.section_('Data')
config.Data.inputDataset = curset
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 70
config.Data.outLFNDirBase = outloc
config.Data.publication = True
config.Data.outputDatasetTag = substr1+'_NanoSlimNtuples'+ver
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
config.Data.ignoreLocality=True
config.section_('Site')
config.Site.storageSite = store
config.Site.whitelist = ["T2_US*"] 
