from django.db import models

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, and_
from config import KEY_hg38, KEY_snpsAssociated_annotation

Base = declarative_base()

def createSessionSQL (keyFile):
    engineSQL = create_engine(keyFile, pool_pre_ping=True)
    Sesion = sessionmaker(bind=engineSQL)
    session = Sesion()
    return session

class snpsAssociated_FDR_promotersEPD(Base):
    __tablename__ = "snpsAssociated_FDR_promotersEPD"

    geneID = sqlalchemy.Column(String(200))
    chrom = sqlalchemy.Column(String(200))
    chromStartPromoter = sqlalchemy.Column(Integer)
    chromEndPromoter = sqlalchemy.Column(Integer)
    chromStartCpG = sqlalchemy.Column(Integer, primary_key=True)
    snpID = sqlalchemy.Column(String(200), primary_key=True)
    promoterID = sqlalchemy.Column(String(200), primary_key=True)

    def get_SNPs_Promoters(_id,_geneId):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_promotersEPD).filter_by(geneID = _geneId).filter_by(snpID=_id).all()
        session.close()
        return data if len(data) > 0 else None

        
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