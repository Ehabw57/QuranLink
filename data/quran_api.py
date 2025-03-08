import requests
import time


class Quran_API:
    BASE_URL = 'https://api.quran.com/api/v4'
    MAX_RETRIES = 5

    @classmethod
    def fetch_surahs(cls):
        try:
            response = requests.get(f"{cls.BASE_URL}/chapters")
            response.raise_for_status()
            print("✅ Fetched surahs successfully")
            return response.json().get('chapters', [])
        except requests.RequestException as e:
            print(f"❌ Error fetching surahs: {e}")
            return []

    @classmethod
    def fetch_ayahs(cls, surah_id):
        retries = 0
        while retries < cls.MAX_RETRIES:
            try:
                response = requests.get(
                    f"{cls.BASE_URL}/verses/by_chapter/{surah_id}",
                    params={
                        'fields': 'text_uthmani,text_imlaei,text_imlaei_simple',
                        'per_page': 300
                        }
                    )
                response.raise_for_status()
                print(f"✅ Fetched verses of surah[{surah_id}] successfully")
                return response.json().get('verses', [])
            except requests.RequestException as e:
                print(f"FETCHING FAILED: {e}. Retrying in 5 seconds...")
                retries += 1
                time.sleep(5)

        print(f"❌Failed to fetch ayahs of surah[{surah_id}]. Limit reached.")
        return []
