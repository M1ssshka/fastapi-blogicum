from contextlib import contextmanager
from pathlib import Path

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self):
        # Получаем путь к корню проекта (4 уровня вверх от database.py)
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        db_path = BASE_DIR / "db.sqlite3"
        self._db_url = f'sqlite:///{db_path}'
        self._engine = create_engine(self._db_url)

    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()
