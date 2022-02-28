from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE']
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

meta = MetaData()

conn =  engine.connect()