"""
Модель таблицы
"""
from typing import Union, Any

from PySide6.QtCore import (QAbstractTableModel, QModelIndex,
                            QPersistentModelIndex, Qt)


class TableModel(QAbstractTableModel):
    "Модель таблицы"

    def __init__(self, data: list[list[Any]],
                 columns: list[str], rows: list[str] | None,
                 edit_indexes: list[int]):
        super().__init__()
        self._data = data
        self._columns = columns
        self.edit_indexes = edit_indexes
        if rows is None:
            rowCount = self.rowCount()
            self._rows = list(str(i) for i in range(rowCount))
        else:
            self._rows = rows

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int = Qt.ItemDataRole.EditRole | Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return f'{value:.2f}'
            return value

    def headerData(self, section: int,
                   orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == \
                Qt.ItemDataRole.DisplayRole:
            return self._columns[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return self._rows[section]

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._data) if self._data else 0

    def columnCount(self,
                    parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._data[0]) if self._data else 0

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if index.column() in self.edit_indexes:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable \
                | Qt.ItemFlag.ItemIsEditable
        else:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def setData(self, index: QModelIndex | QPersistentModelIndex,
                value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            return True
        return False
