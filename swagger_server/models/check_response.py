# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class CheckResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, accepted_num: int=None):  # noqa: E501
        """CheckResponse - a model defined in Swagger

        :param accepted_num: The accepted_num of this CheckResponse.  # noqa: E501
        :type accepted_num: int
        """
        self.swagger_types = {
            'accepted_num': int
        }

        self.attribute_map = {
            'accepted_num': 'accepted_num'
        }

        self._accepted_num = accepted_num

    @classmethod
    def from_dict(cls, dikt) -> 'CheckResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The CheckResponse of this CheckResponse.  # noqa: E501
        :rtype: CheckResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def accepted_num(self) -> int:
        """Gets the accepted_num of this CheckResponse.


        :return: The accepted_num of this CheckResponse.
        :rtype: int
        """
        return self._accepted_num

    @accepted_num.setter
    def accepted_num(self, accepted_num: int):
        """Sets the accepted_num of this CheckResponse.


        :param accepted_num: The accepted_num of this CheckResponse.
        :type accepted_num: int
        """

        self._accepted_num = accepted_num