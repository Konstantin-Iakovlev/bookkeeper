"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime
from bookkeeper.utils import format_date


def get_time_at_now() -> str:
    date = datetime.now()
    return format_date(date)


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: str = field(default_factory=get_time_at_now)
    added_date: str = field(default_factory=get_time_at_now)
    comment: str = ''
    pk: int = 0
