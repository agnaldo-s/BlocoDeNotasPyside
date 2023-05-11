from infra.configs.connection import DBConnectionHandler
from infra.entities.nota import Nota


class NotaRepository:
    def select_all(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).all()
            return data

    def select(self, id):
        with DBConnectionHandler() as db:
            data = db.session.query(Nota).filter(Nota.id_nota == id).first()
            return data

    def insert(self, nota):
        with DBConnectionHandler() as db:
            try:
                db.session.add(nota)
                db.session.commit()
                return 'ok'
            except Exception as e:
                db.session.rollback()
                return e

    def delete(self, id):
        try:
            with DBConnectionHandler() as db:
                db.session.query(Nota).filter(Nota.id_nota == id).delete()
                db.session.commit()
                return 'ok'
        except Exception as e:
            return e

    def update(self, nota:Nota):
        with DBConnectionHandler() as db:
            db.session.query(Nota).filter(Nota.id_nota == nota.id_nota).update(
                {'nome_nota': nota.nome_nota, 'nota': nota.nota})
            db.session.commit()
