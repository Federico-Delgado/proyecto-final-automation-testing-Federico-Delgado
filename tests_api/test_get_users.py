import pytest
import requests

@pytest.mark.api
@pytest.mark.smoke
def test_get_users_lista_completa(users_url):
    """Valida que el endpoint de usuarios devuelva una lista completa con estructura correcta."""
    response = requests.get(users_url)
    
    # Nivel 1: Status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Nivel 2: Headers - verificar que devuelve JSON
    assert 'application/json' in response.headers.get('Content-Type', ''), \
        "Response should be JSON"
    
    # Nivel 3: Estructura JSON - validar que es una lista
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Users list should not be empty"
    
    # Nivel 4: Contenido específico - validar estructura de cada usuario
    required_fields = {'id', 'name', 'email', 'username'}
    for user in data:
        assert required_fields <= set(user.keys()), \
            f"User missing required fields. Has: {set(user.keys())}"
        assert user['id'] > 0, "User ID should be positive"
        assert '@' in user['email'], "Email should be valid"
    
    # Nivel 5: Performance - tiempo de respuesta aceptable
    assert response.elapsed.total_seconds() < 2, \
        f"API too slow: {response.elapsed.total_seconds():.2f}s"
    
    print(f"✅ GET users: {len(data)} usuarios validados en {response.elapsed.total_seconds():.3f}s")

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