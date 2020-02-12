from django.db import models
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc

from config import KEY_snpsAssociated_FDR

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

    def get_SNP_chrom():
        session = createSessionSQL(KEY_snpsAssociated_FDR)
        data = session.query(func.count(snpsAssociated_FDR_chrom.snpID)).all()
        session.close()
        return data[0] if len(data)>0 else None