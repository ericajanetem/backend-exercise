#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import NoAuth
import logging

# Basic full refresh stream
class SpacexExplorerStream(HttpStream, ABC):

    url_base = "https://api.spacexdata.com/v4/"

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        if 'hasNextPage' in response.json():
            nextpage = response.json()['nextPage']
            return {"page": nextpage}
        else:
            return None

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {}
        if next_page_token:
            params.update(next_page_token)
        return params

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        try:
            response_output = response.json()
            if 'docs' in response_output:
                return response_output['docs']
            else:
                return response_output
        except Exception as e:
            logging.error(f"Unknown error encountered: {e}")
            return []

class Launches(SpacexExplorerStream):
    primary_key = "id"
    def __init__(self, authenticator=NoAuth(), **kwargs):
        # self._cursor_field = "date_unix"
        super().__init__(authenticator=authenticator)

    # @property
    # def cursor_field(self) -> str:
    #     return self._cursor_field

    # def get_updated_state(self, current_stream_state: MutableMapping[str, Any], latest_record: Mapping[str, Any]) -> Mapping[str, Any]:
    #     state_value = max(current_stream_state.get(self.cursor_field, 0), latest_record.get(self._cursor_field))
    #     return {self._cursor_field: state_value}

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "launches"

class Starlink(SpacexExplorerStream):
    primary_key = "id"

    def __init__(self, authenticator=NoAuth(), **kwargs):
        super().__init__(authenticator=authenticator)

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "starlink"

class Payloads(SpacexExplorerStream):
    primary_key = "id"

    def __init__(self, authenticator=NoAuth(), **kwargs):
        super().__init__(authenticator=authenticator)

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "payloads"


# Source
class SourceSpacexExplorer(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        try:
            stream = Launches(authenticator=NoAuth())
            response = next(stream.read_records(sync_mode=None))
            return True, None
        except Exception as e:
            return False, str(e)

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        return [Launches(), Starlink(), Payloads()]
