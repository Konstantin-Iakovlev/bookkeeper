"""
Модель бюджета
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense
from bookkeeper.utils import format_date


@dataclass
class Budget:
    """
    Бюджет.
    spent - сумма расходов
    period - название периода
    category - id категории расходов
    limitation - лимит расходов
    pk - id записи в базе данных
    """
    spent: int
    period: Literal["день", "неделя", "месяц"]
    category: int | None = None
    limitation: int | None = None
    pk: int = 0

    def update_spent(self, exp_repo: AbstractRepository[Expense]) -> None:
        """Обновляет потраченную сумму, обращаясь к репозиторию"""
        date = datetime.now()
        if self.period == "день":
            period_exps = exp_repo.get_all(where={"expense_date":
                                           format_date(date)})
        elif self.period == "неделя":
            period_exps = []
            for i in range(date.weekday() + 1):
                weekday = date - timedelta(days=i)
                week_exps = exp_repo.get_all(where={"expense_date":
                                                    format_date(weekday)})
                period_exps += week_exps
        elif self.period == "месяц":
            period_exps = []
            for i in range(date.day):
                monthday = date - timedelta(days=i)
                month_exps = exp_repo.get_all(where={"expense_date":
                                                     format_date(monthday)})
                period_exps += month_exps
        self.spent = sum([exp.amount for exp in period_exps])
