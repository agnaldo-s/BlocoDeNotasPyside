from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, DateTime


class Nota(Base):
    __tablename__ = 'nota'
    id_nota = Column(Integer, autoincrement=True, primary_key=True)
    nome_nota = Column(String(100), nullable=False)
    nota = Column(String(100), nullable=False)
    data_nota = Column(DateTime)

    def __repr__(self):
        return f'Titulo da nota = {self.nome_nota}, id = {self.id_nota}'
