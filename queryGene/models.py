from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from config import KEY_snpsAssociated_annotation, KEY_snpsAssociated_FDR, KEY_hg38

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
    description = sqlalchemy.Column(String(500))

    def get_SNPs_Promoters(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(func.count(snpsAssociated_FDR_promotersEPD.snpID), snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).group_by(snpsAssociated_FDR_promotersEPD.snpID).all()
        session.close()
        return data if len(data) > 1 else None

class snpsAssociated_FDR_enhancers(Base):
    __tablename__ = "snpsAssociated_FDR_enhancers_filtered"

    snpID = sqlalchemy.Column(String(20), primary_key=True)
    geneID = sqlalchemy.Column(String(20), primary_key=True)
    numOverlaps = sqlalchemy.Column(String(20))

    def get_Enhancers(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(snpsAssociated_FDR_enhancers).filter_by(geneID=_id).order_by(snpsAssociated_FDR_enhancers.numOverlaps.desc()).limit(20).all()
        session.close()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_trafficLights(Base):
    __tablename__ = "snpsAssociated_FDR_trafficLights_filtered"

    snpID = sqlalchemy.Column(String(20), primary_key=True)
    gene = sqlalchemy.Column(String(20), primary_key=True)
    numOverlaps = sqlalchemy.Column(String(20))

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