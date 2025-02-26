running the backend
```bash
python3 -m venv ./{venv_name}
source {venv_name}/bin/activate
pip3 install -r requerments.txt
python3 populate_data.py
fastapi dev app.py
```
