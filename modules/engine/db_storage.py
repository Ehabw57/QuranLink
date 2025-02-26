from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from modules.ayahs import Ayahs
from modules.surahs import Surahs, Base


class DBStorage:
    """Handles database storage using SQLAlchemy."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database connection and session."""
        db = "sqlite:///data/quran.db"
        self.__engine = create_engine(db)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def new(self, obj):
        """Adds an object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commits all added objects to the database"""
        self.__session.commit()

    def close(self):
        """Closes the session"""
        self.__session.remove()

    def get_surahs(self):
        """
        Retrieve all Surahs from the database.
        :return: A list of Surah objects.
        """
        return self.__session.query(Surahs).all()

    def get_ayah_id(self, pagination: str):
        try:
            surah_id, ayah_number = map(int, pagination.split(':'))
        except (ValueError, IndexError):
            return None

        ayah = self.__session.query(Ayahs.id).filter(
                Ayahs.surah_id == surah_id, Ayahs.number == ayah_number).first()

        return ayah.id if ayah else None

    def get_ayah_by_id(self, ayah_id):
        return self.__session.query(Ayahs).filter(Ayahs.id == ayah_id).first()

    def retrive_range(self, range_type, start, end):
        if range_type == 'ayah_key':
            return self.__session.query(Ayahs).filter(Ayahs.id >= start, Ayahs.id <= end).all()
        elif range_type == 'page':
            return self.__session.query(Ayahs).filter(Ayahs.page >= start, Ayahs.page <= end).all()
        else:
            return self.__session.query(Ayahs).filter(Ayahs.juz >= start, Ayahs.juz <= end).all()
