from abc import ABC, abstractmethod
import requests


class BaseConnection(ABC):
    @abstractmethod
    def connect(self):
        """
        Base method for connecting to the data source.
        """
        raise NotImplementedError()

    def request(
        self,
        url: str,
        method: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ):
        """
        Method to make a request to a given url.

        :param url: The url to make the request to.
        :param method: The HTTP method to use.
        :param params: The parameters to send with the request.
        :param data: The data to send
        :param headers: The headers to send with the request.

        :return: The response object.
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            raise e
