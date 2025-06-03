"""
database.py
Configuração da conexão com o banco de dados SQLite usando SQLAlchemy,
criação do engine, sessão e base declarativa para os modelos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

# Criação do engine de conexão com o banco, com parâmetro para permitir multithread
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a classe de sessão para interação com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para definir os modelos ORM (classes que representam tabelas)
Base = declarative_base()