
import pytest
from unittest.mock import Mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def test_create_doc():
    dao = Mock()
    dao.create()