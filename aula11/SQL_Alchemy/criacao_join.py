from sqlalchemy import create_engine, Column, Integer, String, DateTime, select
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Documento(Base):
    __tablename__ = 'documentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    origem = Column(String, nullable=False)
    status = Column(String, nullable=False, default='pendente')
    num_tokens = Column(Integer)
    criado_em = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Documento(id={self.id}, nome='{self.nome}', origem='{self.origem}', status='{self.status}', num_tokens={self.num_tokens}, criado_em={self.criado_em})>"

class Token(Base):
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Token(id={self.id}, documento_id={self.documento_id}, token='{self.token}', criado_em={self.criado_em})>"
    
engine = create_engine('postgresql://postgres:myfamili@localhost/postgres', echo=False)
Base.metadata.create_all(engine)
print('Tabela criada.')

#Insert dos dados de tokens
tokens = [
    Token(documento_id=1, token='token1'),
    Token(documento_id=1, token='token2'),
    Token(documento_id=1, token='token3'),
    Token(documento_id=2, token='token4'),
    Token(documento_id=2, token='token5'),
    Token(documento_id=3, token='token6')
]

with Session(engine) as session:
    session.add_all(tokens)
    session.commit()
    print('Registro inserido.')
    
# Fazer left join das tabelas
with Session(engine) as session:
    registros = session.query(Token).outerjoin(Documento, Token.documento_id == Documento.id).all()
    print('Registros do join:')
    for registro in registros:
        print(registro)
        
#Left Join
with Session(engine) as session:
    stmt = select(Token, Documento).join(Documento, Token.documento_id == Documento.id, isouter=True)
    registros = session.execute(stmt).all()
    print('Registros do left join:')
    for registro in registros:
        print(registro)