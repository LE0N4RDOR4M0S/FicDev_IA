from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session 
# ── Engine: aponta para o banco ──────────────────────────────
# SQLite local (arquivo):
engine = create_engine('sqlite:///pipeline.db', echo=False)
# echo=True: imprime o SQL gerado — útil para depuração
 
# Outros bancos (mesmo código ORM):
# PostgreSQL: 'postgresql://user:senha@localhost/dbname'
# MySQL:      'mysql+pymysql://user:senha@localhost/dbname'
# Memória:    'sqlite:///:memory:'  ← ideal para testes
 
# ── Base: classe mãe de todos os modelos ─────────────────────
class Base(DeclarativeBase):
    pass
 
# ── Session: unidade de trabalho ─────────────────────────────
# Session agrupa operações em uma transação
# commit() persiste, rollback() desfaz, close() libera conexão
session = Session(engine)
