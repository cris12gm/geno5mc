from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from config import KEY_snpsAssociated_annotation, KEY_snpsAssociated_FDR

Base = declarative_base()

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

    def get_SNPs_Promoters(_id):
        data = session_snpsAssociated_FDR_annotation.query(func.count(snpsAssociated_FDR_promotersEPD.snpID), snpsAssociated_FDR_promotersEPD).filter_by(geneID=_id).group_by(snpsAssociated_FDR_promotersEPD.snpID).all()
        return data if len(data) > 1 else None

class snpsAssociated_FDR_enhancers(Base):
    __tablename__ = "snpsAssociated_FDR_enhancers_filtered"

    snpID = sqlalchemy.Column(String(20), primary_key=True)
    geneID = sqlalchemy.Column(String(20), primary_key=True)
    numOverlaps = sqlalchemy.Column(String(20))

    def get_Enhancers(_id):
        data = session_snpsAssociated_FDR_annotation.query(snpsAssociated_FDR_enhancers).filter_by(geneID=_id).order_by(snpsAssociated_FDR_enhancers.numOverlaps.desc()).limit(20).all()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_trafficLights(Base):
    __tablename__ = "snpsAssociated_FDR_trafficLights_filtered"

    snpID = sqlalchemy.Column(String(20), primary_key=True)
    gene = sqlalchemy.Column(String(20), primary_key=True)
    numOverlaps = sqlalchemy.Column(String(20))

    def get_trafficLights(_id):
        data = session_snpsAssociated_FDR_annotation.query(snpsAssociated_FDR_trafficLights).filter_by(gene=_id).all()
        session_snpsAssociated_FDR_annotation.close()
        return data if len(data) > 0 else None

engine_snpsAssociated_FDR_annotation = create_engine(KEY_snpsAssociated_annotation)
Sesion_snpsAssociated_FDR_annotation = sessionmaker(bind=engine_snpsAssociated_FDR_annotation)
session_snpsAssociated_FDR_annotation = Sesion_snpsAssociated_FDR_annotation()

class getGeneID(Base):
    __tablename__ = "geneID"

    geneID = sqlalchemy.Column(String(200), primary_key=True)

    def get_Genes(_id):
        data = session_snpsAssociated_FDR_annotation.query(getGeneID).filter_by(geneID=_id).all()
        session_snpsAssociated_FDR_annotation.close()
        return data[0] if len(data) is 1 else None

engine_snpsAssociated_FDR = create_engine(KEY_snpsAssociated_FDR)
Sesion_snpsAssociated_FDR = sessionmaker(bind=engine_snpsAssociated_FDR)
session_snpsAssociated_FDR = Sesion_snpsAssociated_FDR()

class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"

    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))
    chromStart = sqlalchemy.Column(Integer)

    def get_SNP_chrom(_id):
        data = session_snpsAssociated_FDR.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        session_snpsAssociated_FDR.close()
        return data[0] if len(data) is 1 else None