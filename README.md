
# Flash

Flash is a web application that visualizes lightning data for Sweden from [https://www.smhi.se/](SMHI) using interactive maps and charts.
An heatmap for each year is generated.

## Features

- Interactive map with lightning markers and heatmaps (Leaflet)
- Lightning statistics and trends (Highcharts)
- Data table with monthly and yearly lightning counts (DataTables + Bootstrap 5)
- Responsive design using Bootstrap 5
- Data is collected daily

## Installation

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd flash
    ```

2. Create and activate a Python virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Start the Flask development server:

```bash
export FLASK_APP=flash_emitter.py
export FLASK_DEBUG=1  # Optional for debug mode
flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project Structure

- `flash_collector.py` - Application to fetch data
- `flash_emitter.py` - Main Flask application
- `templates/` - HTML templates (`index.html`, `heatmap.html`)
- `static/` - Static files (JS, CSS, data files)
- `requirements.txt` - Python dependencies

## Data

Lightning data is fetched from [https://www.smhi.se/data](SMHI) and stored in JSON files in the `static` directory.
An example of usage is available at [https://www.viltstigen.se/flash](Vilststigen).

## Notes

- This project uses a development server. For production, use a WSGI server like Gunicorn or uWSGI.
- All third-party JS/CSS libraries are loaded via CDN.

## License

MIT License

## Author

Mats Melander