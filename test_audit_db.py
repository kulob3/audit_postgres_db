import os
import stat
import tempfile
import datetime
import pytest
from audit_db import check_permissions, check_cert_expiry

# --- Тесты для check_permissions ---
def test_check_permissions_valid():
    with tempfile.NamedTemporaryFile() as f:
        os.chmod(f.name, 0o600)
        result, mode = check_permissions(f.name, (0o600,))
        assert result is True
        assert mode == "0o600"

def test_check_permissions_invalid():
    with tempfile.NamedTemporaryFile() as f:
        os.chmod(f.name, 0o666)
        result, mode = check_permissions(f.name, (0o600,))
        assert result is False
        assert mode == "0o666"

def test_check_permissions_not_found():
    result, mode = check_permissions("/non/existent/file", (0o600,))
    assert result is False
    assert mode == "File not found"

# --- Тест для сертификата ---
def test_check_cert_expiry_valid():
    # Используем системный демо-сертификат (или свой путь)
    cert_path = "/etc/ssl/certs/ssl-cert-snakeoil.pem"
    if os.path.exists(cert_path):
        valid, message = check_cert_expiry(cert_path)
        assert isinstance(valid, bool)
        assert "Valid until" in message or "Expired" in message
    else:
        pytest.skip("Сертификат отсутствует")
