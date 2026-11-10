import requests 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.config import load_indicators_config

CONFIG = load_indicators_config

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

    def get_matches(self, season: int) -> dict:

        response = self.session.get(
            f"{self.BASE_URL}/competitions/PD/matches",
            params={"season": season},
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict) or not isinstance(
            data.get("matches"), list
        ):
            raise ValueError("Formato de respuesta inesperado")

        return data

    def close(self):
        self.session.close()
