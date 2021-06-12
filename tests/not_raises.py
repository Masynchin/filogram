from contextlib import contextmanager

import pytest


@pytest.fixture
def not_raises():
    @contextmanager
    def _not_raises(exception):
        try:
            yield
        except exception:
            raise pytest.fail(f"DID RAISE {exception}")

    return _not_raises
