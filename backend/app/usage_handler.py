from app.calculate_credit_used_by_text import calculate_credit_used_by_text
from app.models import Message, Usage
from app.orbital_api_client import OrbitalAPIClient


class UsageHandler:
    def __init__(self, api_client: OrbitalAPIClient):
        self.api_client = api_client

    def get_usages_for_current_period(self) -> list[Usage]:
        """
        Fetches all messages for the current period and calculates usage for each message.
        In case there is a report generated, we use credit_used from the report.
        Otherwise, we calculate credits_used based on the text of the message.
        """
        messages = self.api_client.get_messages_for_current_period()

        usages = []
        for message in messages:
            if message.report_id:
                usage = self._get_usage_by_report(message)
                usages.append(usage)
            else:
                usage = self._get_usage_by_text(message)
                usages.append(usage)
        return usages

    def _get_usage_by_text(self, message: Message) -> Usage:
        credits_used = calculate_credit_used_by_text(message.text)
        return Usage(
            message_id=message.id,
            timestamp=message.timestamp,
            report_name=None, # We get usage by text when there is no report
            credits_used=credits_used,
        )

    def _get_usage_by_report(self, message: Message) -> Usage:
        report_response = self.api_client.get_report(message.report_id)
        report = report_response.report
        if not report or report_response.status_code == 404:
            # In case the report is not found, we fallback to calculating usage by text
            return self._get_usage_by_text(message)
        return Usage(
            message_id=message.id,
            timestamp=message.timestamp,
            report_name=report.name,
            credits_used=report.credit_cost
        )