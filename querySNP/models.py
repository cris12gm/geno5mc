from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc
from config import KEY_snpsAssociated_FDR, KEY_snpsAssociated_annotation

Base = declarative_base()

def createSessionSQL (keyFile):
    engineSQL = create_engine(keyFile, pool_pre_ping=True)
    Sesion = sessionmaker(bind=engineSQL)
    session = Sesion()
    return session


class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"

    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))
    chromStart = sqlalchemy.Column(Integer)
    reference = sqlalchemy.Column(String(1))
    alternative = sqlalchemy.Column(String(1))
    hetero = sqlalchemy.Column(String(1))

    def get_SNP_chrom(_id):
        session = createSessionSQL(KEY_snpsAssociated_FDR)
        data = session.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        session.close()
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
            session = createSessionSQL(KEY_snpsAssociated_FDR)
            data = session.query(snpsAssociated_FDR_chr).filter_by(snpID=snpID).all()
            session.close()
            snpsAssociated_FDR_chr.metadata.clear()
            
            return data

    return snpsAssociated_FDR_chr

##################################


class snpsAssociated_FDR_promotersEPD(Base):
    __tablename__ = "snpsAssociated_FDR_promotersEPD"

    geneID = sqlalchemy.Column(String(200))
    chrom = sqlalchemy.Column(String(200))
    chromStartPromoter = sqlalchemy.Column(Integer)
    chromEndPromoter = sqlalchemy.Column(Integer)
    chromStartCpG = sqlalchemy.Column(Integer, primary_key=True)
    snpID = sqlalchemy.Column(String(200), primary_key=True)
    promoterID = sqlalchemy.Column(String(200), primary_key=True)

    def get_Promoters(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(func.count(snpsAssociated_FDR_promotersEPD.geneID).label('total'), snpsAssociated_FDR_promotersEPD).filter_by(snpID=_id).group_by(snpsAssociated_FDR_promotersEPD.geneID).order_by(desc('total')).all()
        session.close()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_enhancers(Base):
    __tablename__ = "snpsAssociated_FDR_enhancersAll"

    chrom = sqlalchemy.Column(String(255))
    chromStart = sqlalchemy.Column(Integer)
    chromEnd = sqlalchemy.Column(Integer)
    enhancerID = sqlalchemy.Column(String(20), primary_key=True)
    genesID = sqlalchemy.Column(String(500))
    chromStartCpG = sqlalchemy.Column((Integer), primary_key=True)
    snpID = sqlalchemy.Column(String(20), primary_key=True)

    def get_Enhancers(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(func.count(snpsAssociated_FDR_enhancers.enhancerID).label('total'),snpsAssociated_FDR_enhancers).filter_by(snpID=_id).group_by(snpsAssociated_FDR_enhancers.enhancerID).order_by(desc('total')).all()
        
        session.close()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_trafficLights(Base):
    __tablename__ = "snpsAssociated_FDR_trafficLights"

    chrom = sqlalchemy.Column(String(30), primary_key=True)
    chromStartTL = sqlalchemy.Column(Integer, primary_key=True)
    gene = sqlalchemy.Column(String(100), primary_key=True)
    snpID = sqlalchemy.Column(String(20), primary_key=True)

    def get_trafficLights(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(func.count(snpsAssociated_FDR_trafficLights.gene).label('total'),snpsAssociated_FDR_trafficLights).filter_by(snpID=_id).group_by(snpsAssociated_FDR_trafficLights.gene).order_by(desc('total')).all()
        session.close()
        return data if len(data) > 0 else None

class getSNPID(Base):
    __tablename__ = "snpsID"

    snpID = sqlalchemy.Column(String(20), primary_key=True)

    def get_SNP(_id):
        session = createSessionSQL (KEY_snpsAssociated_annotation)
        data = session.query(getSNPID).filter_by(snpID=_id).all()
        session.close()
        return data if len(data) > 0 else None