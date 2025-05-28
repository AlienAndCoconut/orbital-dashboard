from functools import lru_cache

import httpx
from app.models import Message, Report, ReportResponse


class OrbitalAPIClient:
    def __init__(self, base_url: str = "https://owpublic.blob.core.windows.net"):
        self.base_url = base_url

    def get_messages_for_current_period(self) -> list[Message]:
        url = f'{self.base_url}/tech-task/messages/current-period'
        response = httpx.get(url)

        # Throws assertion error if the response status code is not 200
        assert response.status_code == 200, f"Failed to fetch messages for current period: {response.status_code}"

        json_data = response.json()
        return [Message(**message) for message in json_data["messages"]]

    @lru_cache()
    def get_report(self, id: int) -> ReportResponse:
        url = f'{self.base_url}/tech-task/reports/{id}'
        response = httpx.get(url)
        if response.status_code == 404:
            return ReportResponse(report=None, status_code=404)

        assert response.status_code == 200, f"Failed to fetch report {id} with: {response.status_code}"
        json_data = response.json()
        
        return ReportResponse(
            report=Report(**json_data),
            status_code=response.status_code
        )