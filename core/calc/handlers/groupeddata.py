"""
Class GroupedDataHandler provides methods to deal with grouped data.
"""

import linecache
import os

import pandas as pd

from .. import data_converters

from ._base import BaseDataHandler

FILE_EXTENSION_DEFAULT = 'groups'


class GroupedDataHandler(BaseDataHandler):

    def __init__(self, did, group_ids=None):
        """
        Initialization.

        :param did: Dataset sample id.
        :type did: int/str
        :param group_ids: List of [hierarchical] group ids.
        :type group_ids: list/None
        """
        super().__init__(did=did)

        self._file_name = self._get_full_file_name(group_ids=group_ids)
        self._groups = []

    def _get_full_file_name(self, group_ids=None):
        """
        Form full file name for data groups storing.

        :param group_ids: List of [hierarchical] group ids.
        :type group_ids: list/None
        :return: Full file name.
        :rtype: str
        """
        group_ids = group_ids or []
        return os.path.join(
            self._get_full_dir_name(),
            '{}{}.{}'.format(
                self._did,
                ''.join(['.group{}'.format(i) for i in group_ids]),
                FILE_EXTENSION_DEFAULT))

    def set_file_name(self, group_ids):
        """
        Set updated storage file name according to the new group ids.

        :param group_ids: List of [hierarchical] group ids.
        :type group_ids: list/None
        """
        self._file_name = self._get_full_file_name(group_ids=group_ids)

    def set_groups(self, dataset, groups_metadata, save_to_file=False):
        """
        Create groups according to the initial dataset and groups metadata.

        :param dataset: Initial dataset sample.
        :type dataset: pandas.DataFrame
        :param groups_metadata: List of dicts per group.
        :type groups_metadata: list
        :param save_to_file: Flag to store data groups into the file.
        :type save_to_file: bool
        """
        del self._groups[:]
        for item in groups_metadata:
            self._groups.append(pd.DataFrame(
                dataset[dataset.index.isin(item['group_indexes'])]))

        if save_to_file:
            self._remove_file(file_name=self._file_name)
            with open(self._file_name, 'w') as f:
                for group in self._groups:
                    f.write('{}\n'.format(group.to_json(orient='table')))

    # TODO: Check the correctness of group_id and corresponding extracted data.
    def get_group(self, group_id):
        """
        Get the group according to the provided id.

        :param group_id: Group id (order number or line number in file).
        :type group_id: int
        :return: Group of data objects from the original dataset sample.
        :rtype: pandas.DataFrame
        """
        if self._groups:
            output = self._groups[group_id]
        else:
            output = data_converters.table_to_df(
                linecache.getline(self._file_name, group_id + 1))

        return output
