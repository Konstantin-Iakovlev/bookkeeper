"""
Тесты для бюджета
"""
from datetime import datetime, timedelta
import pytest

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import format_date

@pytest.fixture
def repo_exp():
    return MemoryRepository[Expense]()

# def test_create_object():
#     b = Budget(1000, "day")
#     assert b.limitation == 1000
#     assert b.pk == 0
#     assert b.period == "day"
#     assert b.spent == 0

#     b = Budget(limitation=1000, period="week", spent=100)
#     assert b.limitation == 1000
#     assert b.pk == 0
#     assert b.period == "week"
#     assert b.spent == 100

#     with pytest.raises(ValueError):
#         b = Budget(limitation=1000, period="century")


# def test_can_add_to_repo(repo):
#     b = Budget(100, 'день')
#     pk = repo.add(b)
#     assert b.pk == pk

def test_update_spent_day(repo_exp):
    b = Budget(0, "день")
    for _ in range(3):
        e = Expense(100, 1)
        repo_exp.add(e)
    b.update_spent(repo_exp)
    assert b.spent == 300

def test_update_spent_month(repo_exp):
    b = Budget(0, "месяц")
    date = datetime.now()
    for i in range(min(3, date.day)):
        e = Expense(100, 1, expense_date=format_date(date - timedelta(days=i + 1)))
        repo_exp.add(e)
    b.update_spent(repo_exp)
    assert b.spent == 100 * min(3, date.day)

def test_update_spent_week(repo_exp):
    b = Budget(0, "неделя")
    date = datetime.now()
    monday = date - timedelta(days=date.weekday())
    for i in range(date.weekday() + 1):
        day = monday + timedelta(days=i)
        e = Expense(100, 1, expense_date=format_date(day))
        repo_exp.add(e)
    b.update_spent(repo_exp)
    assert b.spent == (date.weekday() + 1) * 100
