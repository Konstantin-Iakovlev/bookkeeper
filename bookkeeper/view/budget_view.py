"""
Модуль для описания таблицы бюджета
"""

from typing import Any
from PySide6 import QtWidgets
from bookkeeper.view.table_model import TableModel


class BudgetTableView(QtWidgets.QTableView):
    "Графическое представление бюджета"

    def set_budget_table(self,
                         data: list[list[Any]]) -> None:
        "Установить модель таблицы бюджета"
        columns = 'Сумма Бюджет'.split()
        rows = 'День Неделя Месяц'.split()
        edit_indexes = [1]
        self.item_model = TableModel(data, columns, rows, edit_indexes)
        self.setModel(self.item_model)
        self.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch)

    def get_all_restricts(self) -> list[str]:
        """Получить все ограничения"""
        data: list[str] = []
        for row in range(self.item_model.rowCount()):
            data.append(self.item_model.index(row, 1).data())
        return data
