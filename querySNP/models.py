from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from config import KEY_snpsAssociated_FDR, KEY_snpsAssociated_annotation

Base = declarative_base()

engine_snpsAssociated_FDR = create_engine(KEY_snpsAssociated_FDR)
Sesion_snpsAssociated_FDR = sessionmaker(bind=engine_snpsAssociated_FDR)
session_snpsAssociated_FDR = Sesion_snpsAssociated_FDR()

class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"

    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))

    def get_SNP_chrom(_id):
        data = session_snpsAssociated_FDR.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        return data[0] if len(data) is 1 else None


def snpsAssociated_FDR_chr_table(chrID):
    class snpsAssociated_FDR_chr(Base):
        __tablename__ = 'snpsAssociated_FDR_{chrID}'.format(chrID=str(chrID))

        chrom = sqlalchemy.Column(String(5))
        chromStart = sqlalchemy.Column(Integer, primary_key=True)
        snpID = sqlalchemy.Column(String(10), primary_key=True)
        chromStartSNP = sqlalchemy.Column(Integer)
        refBase = sqlalchemy.Column(String(2))
        altBase = sqlalchemy.Column(String(2))
        hetero = sqlalchemy.Column(String(2))
        uRefBase = sqlalchemy.Column(Integer)
        uAltBase = sqlalchemy.Column(Integer)
        uHetero = sqlalchemy.Column(Integer)
        mRefBase = sqlalchemy.Column(Integer)
        mAltBase = sqlalchemy.Column(Integer)
        mHetero = sqlalchemy.Column(Integer)
        iRefBase = sqlalchemy.Column(Integer)
        iAltBase = sqlalchemy.Column(Integer)
        iHetero = sqlalchemy.Column(Integer)
        other = sqlalchemy.Column(Integer)
        methCount = sqlalchemy.Column(Integer)
        numSamples = sqlalchemy.Column(Integer)
        pValue = sqlalchemy.Column(Float)
        qValue = sqlalchemy.Column(Float)

        def get_Associated(snpID):
            data = session_snpsAssociated_FDR.query(snpsAssociated_FDR_chr).filter_by(snpID=snpID).all()
            snpsAssociated_FDR_chr.metadata.clear()
            return data

    return snpsAssociated_FDR_chr

##################################

engine_snpsAssociated_FDR_annotation = create_engine(KEY_snpsAssociated_annotation)
Sesion_snpsAssociated_FDR_annotation = sessionmaker(bind=engine_snpsAssociated_FDR_annotation)
session_snpsAssociated_FDR_annotation = Sesion_snpsAssociated_FDR_annotation()

class snpsAssociated_FDR_promotersEPD(Base):
    __tablename__ = "snpsAssociated_FDR_promotersEPD"

    geneID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))
    chromStartPromoter = sqlalchemy.Column(Integer)
    chromEndPromoter = sqlalchemy.Column(Integer)
    chromStartCpG = sqlalchemy.Column(Integer)
    snpID = sqlalchemy.Column(String(200), primary_key=True)
    promoterID = sqlalchemy.Column(String(200), primary_key=True)

    def get_Promoters(_id):
        data = session_snpsAssociated_FDR_annotation.query(func.count(snpsAssociated_FDR_promotersEPD.geneID), snpsAssociated_FDR_promotersEPD).filter_by(snpID=_id).group_by(snpsAssociated_FDR_promotersEPD.geneID).all()
        return data if len(data) > 1 else None

class snpsAssociated_FDR_enhancers(Base):
    __tablename__ = "snpsAssociated_FDR_enhancers"

    chrom = sqlalchemy.Column(String(200))
    chromStartEnhancer = sqlalchemy.Column(Integer)
    chromEndEnhancer = sqlalchemy.Column(Integer)
    nameEnhancer = sqlalchemy.Column(String(100), primary_key=True)
    genesEnhancer = sqlalchemy.Column(String(1000), primary_key=True)
    chromStartCpG = sqlalchemy.Column(Integer)
    snpID = sqlalchemy.Column(String(200), primary_key=True)

    def get_Enhancers(_id):
        data = session_snpsAssociated_FDR_annotation.query(func.count(snpsAssociated_FDR_enhancers.nameEnhancer), snpsAssociated_FDR_enhancers).filter_by(snpID=_id).group_by(snpsAssociated_FDR_enhancers.nameEnhancer).all()
        return data if len(data) > 1 else None