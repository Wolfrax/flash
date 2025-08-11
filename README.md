
Install virtual environment and requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use a flask server for local usage

```bash
export FLASK_APP=flash_emitter.py
export FLASK_DEBUG=1  # Optional
flask run
 * Serving Flask app 'flash_emitter.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
127.0.0.1 - - [30/Jul/2025 14:57:58] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jul/2025 14:57:59] "GET /flash/flash_meta.json HTTP/1.1" 200 -
127.0.0.1 - - [30/Jul/2025 14:57:59] "GET /flash/flash_stats.json HTTP/1.1" 200 -
127.0.0.1 - - [30/Jul/2025 14:57:59] "GET /flash/flash_latest.json HTTP/1.1" 200 -
```
