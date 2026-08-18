from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
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

engine = create_engine('postgresql://postgres:myfamili@localhost/postgres', echo=False)
Base.metadata.create_all(engine)
print('Tabela criada.')

#Insert dos dados de documentos
documentos = Documento(nome='documento1.txt', origem='upload', status='pendente', num_tokens=100)
with Session(engine) as session:
    session.add(documentos)
    session.commit()
    print('Registro inserido.')
    
#Insert em lote
documentos_lote = [
    Documento(nome='documento2.txt', origem='upload', status='pendente', num_tokens=200),
    Documento(nome='documento3.txt', origem='upload', status='pendente', num_tokens=300),
    Documento(nome='documento4.txt', origem='upload', status='pendente', num_tokens=400),
]

with Session(engine) as session:
    session.add_all(documentos_lote)
    session.commit()
    print('Registros em lote inseridos.')

