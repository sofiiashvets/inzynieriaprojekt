from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:password@localhost:5432/study', echo=False, pool_size=50, max_overflow=100)
Base = declarative_base()
# meta = MetaData(engine)
# meta.reflect()

Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
# from urllib.parse import urlparse

# import psycopg2
# result = urlparse("postgresql://postgres:password@localhost/study")
# username = result.username
# password = result.password
# database = result.path[1:]
# hostname = result.hostname
# port = result.port
# connection = psycopg2.connect(
#     database = database,
#     user = username,
#     password = password,
#     host = hostname,
#     port = port
# )
