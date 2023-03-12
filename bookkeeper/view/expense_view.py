"""
Модуль для отображения таблицы расходов
"""

from typing import Any

from PySide6.QtWidgets import QTableView, QHeaderView

from bookkeeper.view.table_model import TableModel


class ExpenseTableView(QTableView):
    "Графическое отображение расходов"

    ids: list[int] = []

    def set_expense_table(self,
                          data: list[list[Any]],
                          ids: list[int]) -> None:
        "Установить модель таблицы расходов"
        columns = 'Дата Сумма Категория Комментарий'.split()
        edit_indexes = list(range(4))
        self.item_model = TableModel(data, columns, None, edit_indexes)
        self.setModel(self.item_model)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().hide()
        self.ids = ids

    def get_selected_expense(self) -> int:
        "Получить номер выбанной записи"
        try:
            id_ = int(self.selectedIndexes()[0].row())
            return self.ids[id_]
        except Exception:
            return 0

    def get_all_expenses(self) -> list[list[Any]]:
        "Получить все записи о расходах"
        data: list[list[Any]] = []
        for row in range(self.item_model.rowCount()):
            row_data: list[Any] = [self.ids[row]]
            for column in range(self.item_model.columnCount()):
                row_data.append(self.item_model.index(row, column).data())
            data.append(row_data)
        return data
