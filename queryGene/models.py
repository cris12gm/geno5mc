from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,desc
from config import KEY_snpsAssociated_annotation, KEY_snpsAssociated_FDR, KEY_hg38

Base = declarative_base()

def createSessionSQL (keyFile):
    engineSQL = create_engine(keyFile, pool_pre_ping=True)
    Sesion = sessionmaker(bind=engineSQL)
    session = Sesion()
    return session

class snpsAssociated_FDR_promotersEPD(Base):
    __tablename__ = "snpsAssociated_FDR_promotersEPD"

    geneID = sqlalchemy.Column(String(50))
    chrom = sqlalchemy.Column(String(5))
    chromStartPromoter = sqlalchemy.Column(Integer)
    chromEndPromoter = sqlalchemy.Column(Integer)
    chromStartCpG = sqlalchemy.Column(Integer,primary_key=True)
    snpID = sqlalchemy.Column(String(20),primary_key=True)
    promoterID = sqlalchemy.Column(String(50),primary_key=True)
    description = sqlalchemy.Column(String(500))

    def get_SNPs_Promoters(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).all()
        session.close()
        return data if len(data) > 1 else None

    def get_Promoters_Gene(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).group_by(snpsAssociated_FDR_promotersEPD.promoterID).all()
        session.close()
        return data if len(data)>0 else None

    def get_PromoterId(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(promoterID=_id).all()
        session.close()
        return data if len(data)>0 else None
    
    def get_Promoter_SNP_Id(_id,_snpid):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(promoterID=_id,snpID=_snpid).all()
        session.close()
        return data if len(data)>0 else None

    def getPromoterIDs(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).group_by(snpsAssociated_FDR_promotersEPD.promoterID,snpsAssociated_FDR_promotersEPD.snpID).all()
        session.close()
        return data if len(data)>0 else None


    def get_SNPs_Promoter(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).group_by(snpsAssociated_FDR_promotersEPD.snpID).all()
        session.close()
        return data if len(data)>0 else None

class snpsAssociated_FDR_enhancers(Base):
    __tablename__ = "snpsAssociated_FDR_enhancers_filtered"

    snpID = sqlalchemy.Column(String(20), primary_key=True)
    geneID = sqlalchemy.Column(String(20), primary_key=True)
    numOverlaps = sqlalchemy.Column(String(20))

    def get_Enhancers(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_enhancers).filter_by(geneID=_id).order_by(snpsAssociated_FDR_enhancers.numOverlaps.desc()).all()
        session.close()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_trafficLights(Base):
    __tablename__ = "snpsAssociated_FDR_trafficLights"

    chrom = sqlalchemy.Column(String(30),primary_key=True)
    chromStartTL = sqlalchemy.Column(Integer(),primary_key=True)
    gene = sqlalchemy.Column(String(100), primary_key=True)
    snpID = sqlalchemy.Column(String(20), primary_key=True)

    def get_trafficLights(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_trafficLights).filter_by(gene=_id).all()
        session.close()
        return data if len(data) > 0 else None

class getGeneID(Base):
    __tablename__ = "geneID"

    geneID = sqlalchemy.Column(String(200), primary_key=True)

    def get_Genes(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(getGeneID).filter_by(geneID=_id).all()
        session.close()
        return data[0] if len(data) is 1 else None

    def getSimilar(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(getGeneID).filter(getGeneID.geneID.like(_id)).all()
        session.close()
        return data 

class getAllPromoters(Base):
    __tablename__ = "promoters_EPD"

    chrom = sqlalchemy.Column(String(255))
    chromStart = sqlalchemy.Column(Integer())
    chromEnd = sqlalchemy.Column(Integer())
    id = sqlalchemy.Column(String(255),primary_key=True)
    strand = sqlalchemy.Column(String(1))
    geneID = sqlalchemy.Column(String(255))

    def getAllPromoters_Gene(_id):
        session = createSessionSQL(KEY_hg38)
        data = session.query(getAllPromoters).filter_by(geneID=_id).order_by(getAllPromoters.geneID).all()
        session.close()
        return data if len(data)>0 else None

class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"

    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))
    chromStart = sqlalchemy.Column(Integer)

    def get_SNP_chrom(_id):
        session = createSessionSQL(KEY_snpsAssociated_FDR)
        data = session.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        session.close()
        return data[0] if len(data) is 1 else None

class getGencode(Base):
    __tablename__ = "gencodeToGeneName"

    gencodeID = sqlalchemy.Column(String(255), primary_key=True)
    geneName = sqlalchemy.Column(String(255))

    def getGencodeID(_id):
        session = createSessionSQL(KEY_hg38)
        data = session.query(getGencode).filter_by(geneName=_id).all()
        session.close()
        if len(data)>0:
            data = data[0].gencodeID
        return data if len(data)>0 else None

class genes(Base):
    __tablename__ = "geneDescriptions"

    geneID = sqlalchemy.Column(String(30),primary_key=True)
    description = sqlalchemy.Column(String(500))

    def get_geneDescription(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(genes).filter_by(geneID=_id).all()
        session.close()
        return data[0] if len(data)>0 else None

class topResultsGenes(Base):
    __tablename__ = "snpsAssociated_FDR_topResultsGene"

    geneID = sqlalchemy.Column(String(100),primary_key=True)
    snpID = sqlalchemy.Column(String(100),primary_key=True)
    classElement = sqlalchemy.Column(String(10))
    score = sqlalchemy.Column(Integer)

    def get_TopResultsGene(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(topResultsGenes).filter_by(geneID=_id).order_by(topResultsGenes.score.desc()).all()
        session.close()
        return data if len(data)>0 else None

class getMethylation(Base):
    __tablename__ = "methRatio"

    id = sqlalchemy.Column(String(30), primary_key=True)
    UMB616_brain = sqlalchemy.Column(Float())
    UMB1158_brain = sqlalchemy.Column(Float())
    UMB1829_brain = sqlalchemy.Column(Float())
    UMB1185_brain = sqlalchemy.Column(Float())
    UMB759_brain = sqlalchemy.Column(Float())
    UMB5180_brain = sqlalchemy.Column(Float())
    GSM1173772_brainCortex = sqlalchemy.Column(Float())
    UMB579_brainDPCNn = sqlalchemy.Column(Float())
    UMB797_brainDPC = sqlalchemy.Column(Float())
    GSM1173778_hues6 = sqlalchemy.Column(Float())
    GSM774850_tCell = sqlalchemy.Column(Float())
    GSM848927_mononuclear = sqlalchemy.Column(Float())
    GSM774849_tCell = sqlalchemy.Column(Float())
    GSM1135081_prefrontalCortex = sqlalchemy.Column(Float())
    laurent_h9 = sqlalchemy.Column(Float())
    laurent_h9_fibroblast = sqlalchemy.Column(Float())
    laurent_foreskin_fibroblast = sqlalchemy.Column(Float())
    myers_gm12878 = sqlalchemy.Column(Float())
    myers_h1_hESC = sqlalchemy.Column(Float())
    smith2_sperm = sqlalchemy.Column(Float())
    smith2_sperm_2 = sqlalchemy.Column(Float())
    roadmap_STL001_adipose = sqlalchemy.Column(Float())
    roadmap_STL002_adipose = sqlalchemy.Column(Float())
    roadmap_STL003_adipose = sqlalchemy.Column(Float())
    roadmap_STL011_liver = sqlalchemy.Column(Float())
    roadmap_ro01549_cd34 = sqlalchemy.Column(Float())
    roadmap_ro02035_cd14 = sqlalchemy.Column(Float())
    roadmap_h1_mesenchymal = sqlalchemy.Column(Float())
    roadmap_ipsdf69 = sqlalchemy.Column(Float())
    roadmap_h9 = sqlalchemy.Column(Float())
    roadmap_hues64 = sqlalchemy.Column(Float())
    roadmap_h1_BMP4mesendoderm = sqlalchemy.Column(Float())
    roadmap_endoderm_hESC = sqlalchemy.Column(Float())
    roadmap_h1_BMP4 = sqlalchemy.Column(Float())
    roadmap_h1 = sqlalchemy.Column(Float())
    roadmap_h1_neuronal = sqlalchemy.Column(Float())
    roadmap_ipsDF19_11 = sqlalchemy.Column(Float())
    roadmap_imr90 = sqlalchemy.Column(Float())
    roadmapFetal_H24943_placenta = sqlalchemy.Column(Float())
    roadmapFetal_H25008_adrenalGland = sqlalchemy.Column(Float())
    roadmapFetal_H24996_muscle = sqlalchemy.Column(Float())
    roadmapFetal_H23769_largeIntestine = sqlalchemy.Column(Float())
    roadmapFetal_H24720_muscle = sqlalchemy.Column(Float())
    N37_colon = sqlalchemy.Column(Float())
    Hs1570_prefrontalCortex = sqlalchemy.Column(Float())
    Hs1832_prefrontalCortex = sqlalchemy.Column(Float())
    Hs813_prefrontalCortex = sqlalchemy.Column(Float())
    ziller_frontalCortex_2 = sqlalchemy.Column(Float())
    ziller_frontalCortex = sqlalchemy.Column(Float())
    ziller_hepg2 = sqlalchemy.Column(Float())
    ziller_colonTumor = sqlalchemy.Column(Float())
    ziller_colon = sqlalchemy.Column(Float())
    ziller_frontalCortex_alzheimer = sqlalchemy.Column(Float())
    ziller_frontalCortex_alzheimer_2 = sqlalchemy.Column(Float())
    GM02316_skinFibroblast = sqlalchemy.Column(Float())
    GM02317_skinFibroblast = sqlalchemy.Column(Float())
    GM02456_skinFibroblast = sqlalchemy.Column(Float())
    GM02555_skinFibroblast = sqlalchemy.Column(Float())

    def getMethCpG(_id):
        session = createSessionSQL(KEY_hg38)
        data = session.query(getMethylation).filter_by(id=_id).all()
        session.close()
        return data[0] if len(data)>0 else None

class getGenotype(Base):

    __tablename__ = "genotypes"

    id = sqlalchemy.Column(String(30), primary_key=True)
    reference = sqlalchemy.Column(String(3))
    alternative = sqlalchemy.Column(String(3))
    UMB616_brain = sqlalchemy.Column(Integer)
    UMB1158_brain = sqlalchemy.Column(Integer)
    UMB1829_brain = sqlalchemy.Column(Integer)
    UMB1185_brain = sqlalchemy.Column(Integer)
    UMB759_brain = sqlalchemy.Column(Integer)
    UMB5180_brain = sqlalchemy.Column(Integer)
    GSM1173772_brainCortex = sqlalchemy.Column(Integer)
    UMB579_brainDPCNn = sqlalchemy.Column(Integer)
    UMB797_brainDPC = sqlalchemy.Column(Integer)
    GSM1173778_hues6 = sqlalchemy.Column(Integer)
    GSM774850_tCell = sqlalchemy.Column(Integer)
    GSM848927_mononuclear = sqlalchemy.Column(Integer)
    GSM774849_tCell = sqlalchemy.Column(Integer)
    GSM1135081_prefrontalCortex = sqlalchemy.Column(Integer)
    laurent_h9 = sqlalchemy.Column(Integer)
    laurent_h9_fibroblast = sqlalchemy.Column(Integer)
    laurent_foreskin_fibroblast = sqlalchemy.Column(Integer)
    myers_gm12878 = sqlalchemy.Column(Integer)
    myers_h1_hESC = sqlalchemy.Column(Integer)
    smith2_sperm = sqlalchemy.Column(Integer)
    smith2_sperm_2 = sqlalchemy.Column(Integer)
    roadmap_STL001_adipose = sqlalchemy.Column(Integer)
    roadmap_STL002_adipose = sqlalchemy.Column(Integer)
    roadmap_STL003_adipose = sqlalchemy.Column(Integer)
    roadmap_STL011_liver = sqlalchemy.Column(Integer)
    roadmap_ro01549_cd34 = sqlalchemy.Column(Integer)
    roadmap_ro02035_cd14 = sqlalchemy.Column(Integer)
    roadmap_h1_mesenchymal = sqlalchemy.Column(Integer)
    roadmap_ipsdf69 = sqlalchemy.Column(Integer)
    roadmap_h9 = sqlalchemy.Column(Integer)
    roadmap_hues64 = sqlalchemy.Column(Integer)
    roadmap_h1_BMP4mesendoderm = sqlalchemy.Column(Integer)
    roadmap_endoderm_hESC = sqlalchemy.Column(Integer)
    roadmap_h1_BMP4 = sqlalchemy.Column(Integer)
    roadmap_h1 = sqlalchemy.Column(Integer)
    roadmap_h1_neuronal = sqlalchemy.Column(Integer)
    roadmap_ipsDF19_11 = sqlalchemy.Column(Integer)
    roadmap_imr90 = sqlalchemy.Column(Integer)
    roadmapFetal_H24943_placenta = sqlalchemy.Column(Integer)
    roadmapFetal_H25008_adrenalGland = sqlalchemy.Column(Integer)
    roadmapFetal_H24996_muscle = sqlalchemy.Column(Integer)
    roadmapFetal_H23769_largeIntestine = sqlalchemy.Column(Integer)
    roadmapFetal_H24720_muscle = sqlalchemy.Column(Integer)
    N37_colon = sqlalchemy.Column(Integer)
    Hs1570_prefrontalCortex = sqlalchemy.Column(Integer)
    Hs1832_prefrontalCortex = sqlalchemy.Column(Integer)
    Hs813_prefrontalCortex = sqlalchemy.Column(Integer)
    ziller_frontalCortex_2 = sqlalchemy.Column(Integer)
    ziller_frontalCortex = sqlalchemy.Column(Integer)
    ziller_hepg2 = sqlalchemy.Column(Integer)
    ziller_colonTumor = sqlalchemy.Column(Integer)
    ziller_colon = sqlalchemy.Column(Integer)
    ziller_frontalCortex_alzheimer = sqlalchemy.Column(Integer)
    ziller_frontalCortex_alzheimer_2 = sqlalchemy.Column(Integer)
    GM02316_skinFibroblast = sqlalchemy.Column(Integer)
    GM02317_skinFibroblast = sqlalchemy.Column(Integer)
    GM02456_skinFibroblast = sqlalchemy.Column(Integer)
    GM02555_skinFibroblast = sqlalchemy.Column(Integer)

    def getGenotypeCpG(_id):
        session = createSessionSQL(KEY_hg38)
        data = session.query(getGenotype).filter_by(id=_id).all()
        session.close()
        return data[0] if len(data)>0 else None