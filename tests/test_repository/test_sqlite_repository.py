import pytest
import sqlite3
from dataclasses import dataclass

from bookkeeper.repository.sqlite_repository import SQLiteRepository

DATABASE_FILE = "database/test_sqlrepo.db"


@pytest.fixture
def custom_class():
    @dataclass
    class Custom():
        field1: int
        field2: str = "test_field2_string"
        pk: int = 0
    return Custom


@pytest.fixture
def create_bd():
    with sqlite3.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute(f"DROP TABLE IF EXISTS custom")
    with sqlite3.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE custom(field1, field2)")
    con.close()


@pytest.fixture
def repo(custom_class, create_bd):
    return SQLiteRepository(db_file=DATABASE_FILE, cls=custom_class)


def test_row2obj(repo):
    row = (11, "test_row2obj")
    obj = repo._row2obj(10, row)
    assert obj.pk == 10
    assert obj.field1 == 11
    assert obj.field2 == "test_row2obj"


def test_crud(repo, custom_class):
    # create
    obj_add = custom_class(field1=1, field2="test_crud")
    pk = repo.add(obj_add)
    assert pk == obj_add.pk
    # read
    obj_get = repo.get(pk)
    assert obj_get is not None
    assert obj_get.pk == obj_add.pk
    assert obj_get.field1 == obj_add.field1
    assert obj_get.field2 == obj_add.field2
    # update
    obj_upd = custom_class(field1=11, field2="test_crud_upd", pk=pk)
    repo.update(obj_upd)
    obj_get = repo.get(pk)
    assert obj_get == obj_upd
    # delete
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class(field1=1, pk=1)
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_update_unexistent(repo, custom_class):
    obj = custom_class(field1=1, pk=100)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class(field1=1, pk=0)
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_unexistent(repo):
    assert repo.get(-1) is None


def test_cannot_delete_unexistent(repo):
    with pytest.raises(ValueError):
        repo.delete(-1)


def test_get_all(repo, custom_class):
    objects = [custom_class(field1=1) for _ in range(3)]
    for o in objects:
        repo.add(o)
    print(objects)
    print(repo.get_all())
    assert objects == repo.get_all()


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class(field1=1)
        o.field1 = i
        o.field2 = 'test'
        repo.add(o)
        objects.append(o)
    assert [objects[0]] == repo.get_all({'field1': 0})
    assert objects == repo.get_all({'field2': 'test'})
