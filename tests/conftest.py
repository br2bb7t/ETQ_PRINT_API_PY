import os
from unittest.mock import MagicMock, patch

os.environ["DB_SQLITE"] = "encrypted_sqlite_connection"
os.environ["AES_KEY"] = "A6MV64w0KUDfg/yaFDcvleKigoA69myrtJZiAiuhLo8="
os.environ["AES_IV"] = "Fi7mx2rjmSggIYMyZhTLbg=="

patch_decrypt = patch("infrastructure.database.decrypt.DecryptService.decrypt", return_value="sqlite:///:memory:")
patch_get_db_session = patch("infrastructure.database.db_context.get_db_session", return_value=MagicMock())

patch_decrypt.start()
patch_get_db_session.start()


def pytest_sessionfinish(session, exitstatus):  # pragma: no cover
    """Stop patches after the test session ends."""
    patch_decrypt.stop()
    patch_get_db_session.stop()
