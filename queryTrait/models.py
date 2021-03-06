from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,desc
from config import KEY_hg38, KEY_snpsAssociated_annotation, KEY_snpsAssociated_FDR

Base = declarative_base()

def createSessionSQL (keyFile):
    engineSQL = create_engine(keyFile, pool_pre_ping=True)
    Sesion = sessionmaker(bind=engineSQL)
    session = Sesion()
    return session

class PhenotypeGenotype(Base):
    __tablename__ = "PheGenI"

    trait = sqlalchemy.Column(String(100), primary_key=True)
    snpID = sqlalchemy.Column(String(30), primary_key=True)
    context = sqlalchemy.Column(String(20))
    gene = sqlalchemy.Column(String(50), primary_key=True)
    geneID = sqlalchemy.Column(String(10))
    gene2 = sqlalchemy.Column(String(50), primary_key=True)
    geneID2 = sqlalchemy.Column(String(10))
    chromosome = sqlalchemy.Column(String(5))
    position = sqlalchemy.Column(Integer)

    def get_All_Traits():
        session = createSessionSQL(KEY_hg38)
        data = session.query(PhenotypeGenotype).group_by(PhenotypeGenotype.trait).all()
        session.close()
        return data if len(data) > 1 else None

class PhenotypeGenotypeFDR(Base):
    __tablename__ = "PheGenI_FDR"

    snpID = sqlalchemy.Column(String(30), primary_key=True)
    trait = sqlalchemy.Column(String(100), primary_key=True)
    
    def get_All_SNP_Trait(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(PhenotypeGenotypeFDR).filter_by(trait=_id).all()
        session.close()
        return data if len(data) > 0 else None

    def get_All_Traits():
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(PhenotypeGenotypeFDR).group_by(PhenotypeGenotypeFDR.trait).all()
        session.close()
        return data if len(data) > 0 else None

class snpsAssociated_FDR_chrom(Base):
    __tablename__ = "snpsAssociated_FDR_chrom"

    snpID = sqlalchemy.Column(String(200), primary_key=True)
    chrom = sqlalchemy.Column(String(200))
    chromStart = sqlalchemy.Column(Integer)
    reference = sqlalchemy.Column(String(1))
    alternative = sqlalchemy.Column(String(1))
    hetero = sqlalchemy.Column(String(1))

    def get_SNP_info(_id):
        session = createSessionSQL(KEY_snpsAssociated_FDR)
        data = session.query(snpsAssociated_FDR_chrom).filter_by(snpID=_id).all()
        session.close()
        return data[0] if len(data) is 1 else None

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
    
    def get_Promoters(_id):
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(func.count(snpsAssociated_FDR_promotersEPD.geneID).label('total'), snpsAssociated_FDR_promotersEPD).filter_by(snpID=_id).group_by(snpsAssociated_FDR_promotersEPD.geneID).order_by(desc('total')).all()
        session.close()
        return data if len(data) > 0 else None

class PhenotypeGenotypeTraits(Base):
    __tablename__ = "PheGenI_traitsDefinition"

    trait = sqlalchemy.Column(String(100), primary_key=True)
    definition = sqlalchemy.Column(String(3000))
    
    def get_All_Traits():
        session = createSessionSQL(KEY_hg38)
        data = session.query(PhenotypeGenotypeTraits).all()
        session.close()
        return data if len(data) > 0 else None
    def get_Trait(_id):
        session = createSessionSQL(KEY_hg38)
        data = session.query(PhenotypeGenotypeTraits).filter_by(trait=_id).all()
        session.close()
        return data[0] if len(data) > 0 else None
