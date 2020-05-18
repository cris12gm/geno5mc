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

class chromosomes(Base):
    __tablename__ = "chromosomes_hg38"

    chrom = sqlalchemy.Column(String(5),primary_key=True)
    length = sqlalchemy.Column(Integer())
    
    def get_All_Chroms():
        session = createSessionSQL(KEY_hg38)
        data = session.query(chromosomes).all()
        session.close()
        return data if len(data)>0 else None