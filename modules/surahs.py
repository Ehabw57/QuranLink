from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, BLOB, String

Base = declarative_base()


class Surahs(Base):
    """
    Represents a Surah (chapter) in the Quran.
    Attributes:
        id (int): Primary key, unique identifier for the Surah.
        name_simple (str): Simple name of the Surah.
        name_complex (str): Complex/official name of the Surah.
        ayahs (relationship): One-to-many relationship with Ayahs.
    """
    __tablename__ = 'surahs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(BLOB, nullable=False)
    en_name = Column(String(16), nullable=False)
    ayahs_count = Column(Integer, nullable=False)

    ayahs = relationship('Ayahs', back_populates='surah',
                         cascade="all, delete-orphan")
