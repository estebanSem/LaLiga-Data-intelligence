import requests 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

        return response.json()
    
    
    def get_matches(self, season: int) -> dict:
        data = self._get(
            "competitions/PD/matches",
            {"season": season}
        )
        if not isinstance(data.get("matches"), list):
            raise ValueError("Respuesta inválida de partidos")
        return data

    def get_teams(self, season: int) -> dict:
        data = self._get(
            "competitions/PD/teams",
            {"season": season}
        )
        if not isinstance(data.get("teams"), list):
            raise ValueError("Respuesta inválida de equipos")
        return data

    def get_competition(self) -> dict:
        return self._get("competitions/PD")

    def get_standings(self, season: int) -> dict:
        data = self._get(
            "competitions/PD/standings",
            {"season": season}
        )
        if not isinstance(data.get("standings"), list):
            raise ValueError("Respuesta inválida de clasificación")
        return data


    def close(self):
        self.session.close()
