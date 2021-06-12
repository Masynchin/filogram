import pytest

from filogram import exceptions
from filogram import file_service


def test_correct_save_file(default_file, not_raises):
    with not_raises(exceptions.IntegrityError):
        file_service.save_file(default_file)


def test_cannot_save_same_file(default_file):
    file_service.save_file(default_file)
    with pytest.raises(exceptions.IntegrityError):
        file_service.save_file(default_file)
