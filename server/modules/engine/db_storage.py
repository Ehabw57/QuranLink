from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from modules.ayahs import Ayahs
from modules.surahs import Surahs, Base


class DBStorage:
    """Handles database storage using SQLAlchemy."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database connection and session."""
        QL_ENV = getenv("QL_ENV")
        DB = "data/quran.db" if QL_ENV != "test" else ":memory:"

        self.__engine = create_engine(f"sqlite:///{DB}")
        Base.metadata.create_all(self.__engine)
        self.__session = self._create_session()

    def _create_session(self):
        """Creates and returns a new scoped session."""
        session_factory = sessionmaker(bind=self.__engine)
        return scoped_session(session_factory)()

    def new(self, obj) -> None:
        """Adds an object to the session."""
        self.__session.add(obj)

    def save(self) -> None:
        """Commits all added objects to the database."""
        self.__session.commit()

    def reset(self) -> None:
        """Drops all tables and recreates them."""
        Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = self._create_session()

    def close(self) -> None:
        """close the sesssion"""
        self.__session.remove()

    def get_surah(self, id=None):
        if not isinstance(id, int):
            return None
        return self.__session.query(Surahs).filter(
                Surahs.id == id).first()

    def get_surahs(self):
        return self.__session.query(Surahs).all()

    def get_ayah_id(self, pagination: str):
        try:
            surah_id, ayah_number = map(int, pagination.split(':'))
        except (AttributeError, ValueError, IndexError):
            return None
        ayah = self.__session.query(Ayahs.id).filter(
                Ayahs.surah_id == surah_id,
                Ayahs.number == ayah_number).first()
        return ayah.id if ayah else None

    def get_ayah_by_id(self, ayah_id=None):
        """retrive an ayah by it's id"""
        return self.__session.query(Ayahs).filter(Ayahs.id == ayah_id).first()

    def get_ayahs_by_id_range(self, start, end):
        return self.__session.query(Ayahs).filter(Ayahs.id.between(start, end)).all()

    def get_ayahs_by_page_range(self, start, end):
        return self.__session.query(Ayahs).filter(Ayahs.page.between(start, end)).all()

    def get_ayahs_by_juz_range(self, start, end):
        return self.__session.query(Ayahs).filter(Ayahs.juz.between(start, end)).all()
