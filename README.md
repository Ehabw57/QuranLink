running the backend
```bash
python3 -m venv ./{venv_name}
source {venv_name}/bin/activate
pip3 install -r requerments.txt
fastapi dev app.py
```
End Points
1-localhost:8000/surahs
return list of all mushaf chapters
2-locahost:8000/verses?range_type=[page, juz, key]&range_value=start:end
return list of specifc verses range base on range_type and values
3-localhost:8000/pages?page=start:end
returns list of Q-A pairs of last_ayah_on page(x):first ayah_on_page(x+1)
