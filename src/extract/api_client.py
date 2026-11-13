import requests
import json

from requests.adapters  import HTTPAdapter
from urllib3.util.retry import Retry

from pathlib    import Path
from datetime   import datetime, timezone

from utils.config import load_indicators_config

CONFIG = load_indicators_config()

class FootballDataClient:

    BASE_URL = CONFIG['API']['base_url']

    def __init__(self, api_key: str):

        if not api_key:
            raise ValueError("La API_KEY es obligatoria")

        self.session = requests.Session()
        self.session.headers.update({
            "X-Auth-Token" : api_key
        })

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429,500,502,503,504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount(
            prefix  = "https://", 
            adapter = adapter
        )

    def _get(self, endpoint: str, params: dict | None = None):

        response = self.session.get(
            f"{self.BASE_URL}/{endpoint}",
            params = params,
            timeout = 30
        )

        response.raise_for_status()

        print("- Datos obtenidos correctamente")

        return response.json()

    def _save_data(self, data, season: str, raw_path: str, option: str):

        timestamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%S%fZ"
        )
        
        output_dir = Path(f"{raw_path}/{season}/{option}")
        output_dir.mkdir(
            parents = True,
            exist_ok = True
        )
    
        output_path = output_dir / (
            f"laliga_matches_{timestamp}.json"
        )
    
        with output_path.open("x", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    
        print(f"- Archivo guardado: {output_path}")
    
        return output_path
    
    def close(self):
        self.session.close()
