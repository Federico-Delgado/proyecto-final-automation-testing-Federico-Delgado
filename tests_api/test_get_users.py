import pytest
import requests
from utils.logger import logger

@pytest.mark.api
@pytest.mark.smoke
def test_get_users_lista_completa(users_url):
    logger.info(f"Ejecutando GET a: {users_url}")
    response = requests.get(users_url)
    
    assert response.status_code == 200
    logger.info("Status code 200 verificado correctamente")
    
    data = response.json()
    assert isinstance(data, list) and len(data) > 0
    logger.info(f"Se obtuvieron {len(data)} usuarios válidos")
    
    assert response.elapsed.total_seconds() < 2
    logger.info(f"Performance OK: {response.elapsed.total_seconds():.3f}s")

@pytest.mark.api
def test_get_user_especifico(users_url):
    """Valida que se pueda obtener un usuario específico por ID."""
    user_id = 1
    response = requests.get(f"{users_url}/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data['id'] == user_id
    assert 'name' in data
    assert 'email' in data
    
    print(f"✅ GET user {user_id}: {data['name']}")

@pytest.mark.api
def test_get_user_inexistente(users_url):
    """Escenario negativo: validar que un ID inexistente devuelve 404."""
    response = requests.get(f"{users_url}/99999")
    
    # JSONPlaceholder devuelve 404 para recursos inexistentes
    assert response.status_code == 404, \
        f"Expected 404 for non-existent user, got {response.status_code}"
    
    print("✅ GET user inexistente: 404 correctamente devuelto")