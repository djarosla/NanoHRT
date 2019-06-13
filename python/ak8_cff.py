import FWCore.ParameterSet.Config as cms
from  PhysicsTools.NanoAOD.common_cff import *
from Configuration.Eras.Modifier_run2_miniAOD_80XLegacy_cff import run2_miniAOD_80XLegacy

# ---------------------------------------------------------


def setupCustomizedAK8(process, runOnMC=False, path=None, Settype=''):
    # recluster Puppi jets, add N-Subjettiness and ECF
    from RecoBTag.MXNet.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsAll as pfDeepBoostedJetTagsAll

    bTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfBoostedDoubleSecondaryVertexAK8BJetTags',
        'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
    ]
    subjetBTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probbb',
    ]
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']

    from PhysicsTools.NanoHRT.jetToolbox_cff import jetToolbox
    jetToolbox(process, 'ak8', 'dummySeq', 'out', associateTask=False,
               PUMethod='Puppi', JETCorrPayload='AK8PFPuppi', JETCorrLevels=JETCorrLevels,
               Cut='pt > 170.0 && abs(rapidity()) < 2.4',
               miniAOD=True, runOnMC=runOnMC,
               addNsub=True, maxTau=4, addEnergyCorrFunc=True,
               addSoftDrop=True, addSoftDropSubjets=True, subJETCorrPayload='AK4PFPuppi', subJETCorrLevels=JETCorrLevels,
               bTagDiscriminators=bTagDiscriminators, subjetBTagDiscriminators=subjetBTagDiscriminators)

    if runOnMC:
        process.ak8GenJetsNoNu.jetPtMin = 100
        process.ak8GenJetsNoNuSoftDrop.jetPtMin = 100

    # DeepAK8
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    from RecoBTag.MXNet.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsProbs, _pfMassDecorrelatedDeepBoostedJetTagsProbs
    '''updateJetCollection(
        process,
        jetSource=cms.InputTag('packedPatJetsAK8PFPuppiSoftDrop'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
        btagDiscriminators=bTagDiscriminators + _pfDeepBoostedJetTagsProbs + _pfMassDecorrelatedDeepBoostedJetTagsProbs,
        postfix='AK8WithPuppiDaughters',
    )'''

    Bdiscs = ['pfDeepFlavourJetTags:probb', 'pfDeepFlavourJetTags:probbb', 'pfDeepFlavourJetTags:probuds', 'pfDeepFlavourJetTags:probg' , 'pfDeepFlavourJetTags:problepb', 'pfDeepFlavourJetTags:probc','pfCombinedInclusiveSecondaryVertexV2BJetTags']

    jetToolbox( process, 'ak8', 'ak8JetSubs', 'out', associateTask=False, 
		updateCollection='packedPatJetsAK8PFPuppiSoftDrop', JETCorrPayload='AK8PFPuppi', JETCorrLevels=JETCorrLevels,
                Cut='pt > 170.0 && abs(rapidity()) < 2.4',
                miniAOD=True, runOnMC=runOnMC,bTagDiscriminators=bTagDiscriminators + _pfDeepBoostedJetTagsProbs + _pfMassDecorrelatedDeepBoostedJetTagsProbs,
		updateCollectionSubjets='selectedPatJetsAK8PFPuppiSoftDropPacked:SubJets', subjetBTagDiscriminators=Bdiscs, 
		subJETCorrPayload='AK4PFPuppi', subJETCorrLevels=JETCorrLevels,postFix='AK8WithPuppiDaughters')





    exst = ''
    process.imageJetsAK8Puppi = cms.EDProducer('ImageProducer',
        src=cms.InputTag('selectedUpdatedPatJetsAK8PFPuppiAK8WithPuppiDaughters'),
        sj=cms.InputTag('selectedUpdatedPatJetsAK8PFPuppiAK8WithPuppiDaughtersSoftDropPacked'),
        sdmcoll=cms.string('ak8PFJetsPuppiSoftDropMass'),
        pb_path=cms.untracked.FileInPath('PhysicsTools/NanoHRT/data/Image/NNtraining_preliminary_01232018.pb'),
        pb_pathMD=cms.untracked.FileInPath('PhysicsTools/NanoHRT/data/Image/NNtraining_preliminary_MD_01232018.pb'),
	stype=cms.string(Settype),
        extex=cms.string(exst),
        isHotVR=cms.bool(False),
        drfac=cms.double(1.0),
    )                           

    # src
    srcJets = cms.InputTag('imageJetsAK8Puppi')

    # jetID
    process.looseJetIdCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version = cms.string('WINTER16'),
                quality = cms.string('LOOSE'),
              ),
              src=srcJets
    )

    process.tightJetIdCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version=cms.string('WINTER17'),
                quality = cms.string('TIGHT'),
              ),
              src=srcJets
    )
    run2_miniAOD_80XLegacy.toModify(process.tightJetIdCustomAK8.filterParams, version="WINTER16")

    process.tightJetIdLepVetoCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version = cms.string('WINTER17'),
                quality = cms.string('TIGHTLEPVETO'),
              ),
              src=srcJets
    )

    process.customAK8WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
        src=srcJets,
        userFloats=cms.PSet(),
        userInts=cms.PSet(
           tightId=cms.InputTag("tightJetIdCustomAK8"),
           tightIdLepVeto=cms.InputTag("tightJetIdLepVetoCustomAK8"),
        ),
    )
    run2_miniAOD_80XLegacy.toModify(process.customAK8WithUserData.userInts,
        looseId=cms.InputTag("looseJetIdCustomAK8"),
        tightIdLepVeto=None,
    )

    process.customAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src=cms.InputTag("customAK8WithUserData"),
        name=cms.string("CustomAK8Puppi"),
        cut=cms.string(""),
        doc=cms.string("customized ak8 puppi jets for HRT"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            jetId=Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int, doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            tau1=Var("userFloat('NjettinessAK8Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            tau2=Var("userFloat('NjettinessAK8Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            tau3=Var("userFloat('NjettinessAK8Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            tau4=Var("userFloat('NjettinessAK8Puppi:tau4')", float, doc="Nsubjettiness (4 axis)", precision=10),
            n2b1=Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN2')", float, doc="N2 with beta=1", precision=10),
            n3b1=Var("userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN3')", float, doc="N3 with beta=1", precision=10),
            msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            btagCSVV2=Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')", float, doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)", precision=10),
            btagHbb=Var("bDiscriminator('pfBoostedDoubleSecondaryVertexAK8BJetTags')", float, doc="Higgs to BB tagger discriminator", precision=10),
            subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 doc="index of second subjet"),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            # BEST Tagger
            itop=Var("userFloat('Image"+exst+":top')", float, doc="Image tagger score top", precision=-1),
            iMDtop=Var("userFloat('ImageMD"+exst+":top')", float, doc="Image tagger score top", precision=-1),
            itopdr=Var("userFloat('Image"+exst+":DRave')", float, doc="Image tagger score top", precision=-1),

        )
    )
    run2_miniAOD_80XLegacy.toModify(process.customAK8Table.variables, jetId=Var("userInt('tightId')*2+userInt('looseId')", int, doc="Jet ID flags bit1 is loose, bit2 is tight"))
    process.customAK8Table.variables.pt.precision = 10

    # add DeepAK8 scores: nominal
    for prob in _pfDeepBoostedJetTagsProbs:
        name = prob.split(':')[1].replace('prob', 'nn')
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add DeepAK8 scores: mass decorrelated
    for prob in _pfMassDecorrelatedDeepBoostedJetTagsProbs:
        name = prob.split(':')[1].replace('prob', 'nnMD')
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    process.customAK8SubJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src=cms.InputTag("selectedPatJetsAK8PFPuppiSoftDropPacked", "SubJets"),
        cut=cms.string(""),
        name=cms.string("CustomAK8PuppiSubJet"),
        doc=cms.string("customized ak8 puppi subjets for HRT"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            btagDeepB=Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')", float, doc="DeepCSV b+bb tag discriminator", precision=10),
            btagCSVV2=Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')", float, doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
        )
    )
    process.customAK8SubJetTable.variables.pt.precision = 10

    process.customizedAK8Task = cms.Task(
        #process.boostedEventShapeJetsAK8Puppi,
        process.imageJetsAK8Puppi,
        #process.imageJetsAK8Puppi1,
        process.tightJetIdCustomAK8,
        process.tightJetIdLepVetoCustomAK8,
        process.customAK8WithUserData,
        process.customAK8Table,
        process.customAK8SubJetTable
        )

    if runOnMC:
        process.customGenJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("CustomGenJetAK8"),
            doc=cms.string("AK8 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenJetAK8Table.variables.pt.precision = 10

        process.customGenSubJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("CustomGenSubJetAK8"),
            doc=cms.string("AK8 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenSubJetAK8Table.variables.pt.precision = 10

        process.customizedAK8Task.add(process.customGenJetAK8Table)
        process.customizedAK8Task.add(process.customGenSubJetAK8Table)

    _customizedAK8Task_80X = process.customizedAK8Task.copy()
    _customizedAK8Task_80X.replace(process.tightJetIdLepVetoCustomAK8, process.looseJetIdCustomAK8)
    run2_miniAOD_80XLegacy.toReplaceWith(process.customizedAK8Task, _customizedAK8Task_80X)

    if path is None:
        process.schedule.associate(process.customizedAK8Task)
    else:
        getattr(process, path).associate(process.customizedAK8Task)
