from django.db import models
from django import forms

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from config import KEY_snpsAssociated_annotation

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