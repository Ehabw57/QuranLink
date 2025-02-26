from data.quran_api import Quran_API
from modules.surahs import Surahs
from modules.ayahs import Ayahs
from modules import Storage


def clean_ayah(ayah):
    """Clean any seprataed tajweed marks"""
    words = ayah.split()
    cleaned = [""]
    for x in range(len(words)):
        if x > 0 and len(words[x]) < 2:
            cleaned[-1] += words[x]
        else:
            cleaned.append(words[x])
    return cleaned[1:]


def populate_data():
    """ Populates the database with Surahs and Ayahs.
    Fetches data from the API, processes it, and inserts it into the database
    """
    surahs = Quran_API.fetch_surahs()
    for s in surahs:
        Storage.new(Surahs(
                name=s['name_arabic'].encode('utf-8'),
                en_name=s['name_simple'],
                ayahs_count=s['verses_count']))
    Storage.save()

    for surah in surahs:
        ayahs = Quran_API.fetch_ayahs(surah['id'])
        for a in ayahs:
            Storage.new(Ayahs(
                    surah_id=surah['id'],
                    number=a['verse_number'],
                    text=clean_ayah(a['text_imlaei']),
                    simple_text=a['text_imlaei_simple'].split(),
                    page=a['page_number'],
                    juz=a['juz_number']))
        Storage.save()
    Storage.close


if __name__ == "__main__":
    populate_data()
