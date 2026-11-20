import pytest
import requests
from datetime import datetime

@pytest.mark.api
@pytest.mark.parametrize("nombre,trabajo", [
    ("Federico QA", "Automation Tester"),
    ("Matias Dev", "Backend Developer"),
    ("Silvia PO", "Product Owner")
])
def test_create_post_con_datos(posts_url, nombre, trabajo):
    """Valida la creación de posts con diferentes datos parametrizados."""
    payload = {
        'title': f'Post de {nombre}',
        'body': f'Trabajo: {trabajo}',
        'userId': 1
    }
    
    response = requests.post(posts_url, json=payload)
    
    # Nivel 1: Status code para creación
    assert response.status_code == 201, \
        f"Expected 201 Created, got {response.status_code}"
    
    # Nivel 2: Headers
    assert 'application/json' in response.headers.get('Content-Type', '')
    
    # Nivel 3: Estructura - debe contener todos los campos enviados + id generado
    data = response.json()
    assert 'id' in data, "Response should contain generated ID"
    assert 'title' in data
    assert 'body' in data
    assert 'userId' in data
    
    # Nivel 4: Contenido - validar que los datos enviados se reflejan
    assert data['title'] == payload['title']
    assert data['body'] == payload['body']
    assert data['userId'] == payload['userId']
    
    # Nivel 5: Performance
    assert response.elapsed.total_seconds() < 1.5, \
        f"POST too slow: {response.elapsed.total_seconds():.2f}s"
    
    print(f"✅ POST creado: ID {data['id']} - {nombre}")