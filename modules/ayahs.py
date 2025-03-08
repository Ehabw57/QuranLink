from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Index, JSON, Boolean
from .surahs import Base


class Ayahs(Base):
    """
    Represents an Ayah (verse) in the Quran.
    Attributes:
        id (int): Primary key, unique identifier for the Ayah.
        surah_id (int): Foreign key referencing the Surah.
        number (int): Ayah number in the Surah.
        text (Json): Ayah text (encoded in UTF-8).
        simple_text (Json): Simplified text (encoded in UTF-8).
        page (int): Page number in the Quran.
        juz (int): Juz (section) number.
    """
    __tablename__ = 'ayahs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surah_id = Column(Integer, ForeignKey('surahs.id'), index=True)
    number = Column(Integer, nullable=False)
    text = Column(JSON, nullable=False)
    simple_text = Column(JSON, nullable=False)
    page = Column(Integer, nullable=False, index=True)
    juz = Column(Integer, nullable=False, index=True)
    rub = Column(Integer, nullable=False, index=True)
    sajdah = Column(Boolean, default=False)

    surah = relationship('Surahs', back_populates='ayahs')

    table_args__ = (Index('idx_ayah_surah_number', 'surah_id', 'number'),)
