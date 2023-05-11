from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.base import Base


class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = 'mysql+pymysql://admin:senhasegura@localhost/notas'
        self.__engine = self.__create_engine()
        self.session = None
        self.__create_database()

    def __create_database(self):

        try:
            self.__engine.connect()
        except BaseException as e:
            if '1049' in str(e):
                new__engine = create_engine(self.__connection_string.rsplit("/", 1)[0])
                conn = new__engine.connect()
                conn.execute(f'CREATE DATABASE IF NOT EXISTS {self.__connection_string.rsplit("/", 1)[1]}')
                conn.close()
                print('Banco criado com sucesso!')
                self.__create_table()
            else:
                raise e

    def __create_table(self):
        engine = create_engine(self.__connection_string, echo=True)
        Base.metadata.create_all(bind=engine)
        print('Tabela criada com sucesso!')

    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        print('Gerando conexão')
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Fechando conexão')
        self.session.close()
