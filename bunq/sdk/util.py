import json
import socket

import requests

from bunq.sdk.client import ApiClient
from bunq.sdk.context import ApiContext, ApiEnvironmentType
from bunq.sdk.exception import BunqException
from bunq.sdk.model.generated import endpoint

__UNIQUE_REQUEST_ID = "uniqueness-is-required"
__FIELD_API_KEY = "ApiKey"
__INDEX_FIRST = 0
__FIELD_RESPONSE = "Response"
__ENDPOINT_SANDBOX_USER = "sandbox-user"

_ERROR_COULD_NOT_CREATE_NEW_SANDBOX_USER = "Could not create new sandbox" \
                                           " user."


def automatic_sandbox_install():
    """
    :rtype: ApiContext
    """

    sandbox_user = __generate_new_sandbox_user()

    return ApiContext(
        ApiEnvironmentType.SANDBOX,
        sandbox_user.api_key,
        socket.gethostname()
    )


def __generate_new_sandbox_user():
    """
    :rtype: endpoint.SandboxUser
    """

    url = ApiEnvironmentType.SANDBOX.uri_base + __ENDPOINT_SANDBOX_USER

    headers = {
        ApiClient.HEADER_REQUEST_ID: __UNIQUE_REQUEST_ID,
        ApiClient.HEADER_CACHE_CONTROL: ApiClient._CACHE_CONTROL_NONE,
        ApiClient.HEADER_GEOLOCATION: ApiClient._GEOLOCATION_ZERO,
        ApiClient.HEADER_LANGUAGE: ApiClient._LANGUAGE_EN_US,
        ApiClient.HEADER_REGION: ApiClient._REGION_NL_NL,
    }

    response = requests.request(ApiClient._METHOD_POST, url, headers=headers)

    if response.status_code is ApiClient._STATUS_CODE_OK:
        response_json = json.loads(response.text)
        return endpoint.SandboxUser.from_json(
            json.dumps(response_json[__FIELD_RESPONSE][__INDEX_FIRST][
                           __FIELD_API_KEY]))

    raise BunqException(_ERROR_COULD_NOT_CREATE_NEW_SANDBOX_USER)