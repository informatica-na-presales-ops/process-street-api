import dataclasses
import typing
import urllib.parse

import httpx


@dataclasses.dataclass
class ProcessStreetClient:
    api_key: str
    base_url: str = "https://public-api.process.st/api/v1.1"

    def call(self, url: str, method: str = "GET", params: dict | None = None) -> dict:
        headers = {"X-API-Key": self.api_key}
        if params is None:
            params = {}
        with httpx.Client(base_url=self.base_url, headers=headers) as client:
            r = client.request(method, url, params=params)
            r.raise_for_status()
            return r.json()

    @property
    def data_sets(self) -> list["DataSet"]:
        return [DataSet(self, d) for d in self.get_data_sets().get("dataSets")]

    def get_data_sets(self) -> dict:
        return self.call("/data-sets")

    def get_test_auth(self) -> dict:
        return self.call("/testAuth")

    def yield_data_set_records(
        self, data_set_id: str
    ) -> typing.Iterator["DataSetRecord"]:
        params = {}
        has_more = True
        while has_more:
            has_more = False
            response = self.call(f"/data-sets/{data_set_id}/records", params=params)
            yield from (DataSetRecord(r) for r in response.get("records"))
            links = response.get("links")
            for link in links:
                if link.get("name") == "next":
                    next_url = urllib.parse.urlsplit(link.get("href"))
                    params = urllib.parse.parse_qs(next_url.query)
                    has_more = True

    def yield_workflow_form_fields(self, workflow_id: str) -> typing.Iterator[dict]:
        params = {}
        has_more = True
        while has_more:
            has_more = False
            response = self.call(f"/workflows/{workflow_id}/form-fields", params=params)
            yield from response.get("fields")
            links = response.get("links")
            for link in links:
                if link.get("name") == "next":
                    next_url = urllib.parse.urlsplit(link.get("href"))
                    params = urllib.parse.parse_qs(next_url.query)
                    has_more = True

    def yield_workflow_tasks(self, workflow_id: str) -> typing.Iterator[dict]:
        params = {}
        has_more = True
        while has_more:
            has_more = False
            response = self.call(f"/workflows/{workflow_id}/tasks", params=params)
            yield from response.get("tasks")
            links = response.get("links")
            for link in links:
                if link.get("name") == "next":
                    next_url = urllib.parse.urlsplit(link.get("href"))
                    params = urllib.parse.parse_qs(next_url.query)
                    has_more = True

    def yield_workflows(self) -> typing.Iterator[dict]:
        params = {}
        has_more = True
        while has_more:
            has_more = False
            response = self.call("/workflows", params=params)
            yield from response.get("workflows")
            links = response.get("links")
            for link in links:
                if link.get("name") == "next":
                    next_url = urllib.parse.urlsplit(link.get("href"))
                    params = urllib.parse.parse_qs(next_url.query)
                    has_more = True


class DataSet:
    def __init__(self, client: ProcessStreetClient, data: dict) -> None:
        self.client = client
        self.data = data

    @property
    def fields(self) -> list["DataSetField"]:
        return [DataSetField(f) for f in self.data.get("fields")]

    @property
    def id(self) -> str:
        return self.data.get("id")

    @property
    def name(self) -> str:
        return self.data.get("name")

    @property
    def organization_id(self) -> str:
        return self.data.get("organizationId")

    @property
    def records(self) -> typing.Iterator["DataSetRecord"]:
        yield from self.client.yield_data_set_records(self.id)


class DataSetField:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def field_type(self) -> str:
        return self.data.get("fieldType")

    @property
    def id(self) -> str:
        return self.data.get("id")

    @property
    def name(self) -> str:
        return self.data.get("name")


class DataSetRecord:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def cells(self) -> list[dict]:
        return self.data.get("cells")

    @property
    def data_set_id(self) -> str:
        return self.data.get("dataSetId")

    @property
    def id(self) -> str:
        return self.data.get("id")
