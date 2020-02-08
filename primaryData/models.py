from django.db import models
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc
from config import KEY_snpsAssociated_annotation

Base = declarative_base()

def createSessionSQL (keyFile):
    engineSQL = create_engine(keyFile, pool_pre_ping=True)
    Sesion = sessionmaker(bind=engineSQL)
    session = Sesion()
    return session

class samples(Base):
    __tablename__ = "samples"

    SRX = sqlalchemy.Column(String(30), primary_key=True)
    SRP = sqlalchemy.Column(String(30))
    bioSample = sqlalchemy.Column(String(30))
    tissueType = sqlalchemy.Column(String(255))
    totalNumOfReads = sqlalchemy.Column(Integer)
    percentageMethylatedCpG = sqlalchemy.Column(Float)
    percentageUnMethylatedCpG = sqlalchemy.Column(Float)
    positionsVariation = sqlalchemy.Column(Integer)


    def get_all_samples():
        session = createSessionSQL(KEY_snpsAssociated_annotation)
        data = session.query(samples).all()
        session.close()
        return data if len(data)>0 else None