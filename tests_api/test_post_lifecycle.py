import pytest
import requests

@pytest.fixture(scope='module')
def created_post(posts_url):
    """Fixture que crea un post y devuelve sus datos para usar en otros tests."""
    payload = {
        'title': 'Post para testing de ciclo de vida',
        'body': 'Contenido de prueba para validar CRUD completo',
        'userId': 1
    }
    
    response = requests.post(posts_url, json=payload)
    assert response.status_code == 201, f"Failed to create post: {response.status_code}"
    
    return response.json()

@pytest.mark.api
@pytest.mark.e2e
def test_01_post_creado_correctamente(created_post):
    """Valida que el post fue creado con los datos correctos."""
    assert 'id' in created_post
    assert created_post['title'] == 'Post para testing de ciclo de vida'
    assert created_post['body'] == 'Contenido de prueba para validar CRUD completo'
    assert created_post['userId'] == 1
    
    print(f"✅ POST creado con ID: {created_post['id']}")

@pytest.mark.api
@pytest.mark.e2e
def test_02_actualizar_post_parcial(post_by_id_url):
    """Valida que se puede actualizar parcialmente un post (PATCH)."""
    # Usamos un ID existente (1) para garantizar que JSONPlaceholder lo procese correctamente,
    # ya que a veces falla con IDs > 100 en operaciones de actualización.
    post_id = 1
    url = post_by_id_url(post_id)
    
    update_payload = {
        'title': 'Título actualizado por QA'
    }
    
    response = requests.patch(url, json=update_payload)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data['title'] == 'Título actualizado por QA', "PATCH should update the title"
    
    # NOTA: JSONPlaceholder a menudo solo devuelve los campos actualizados en la respuesta 
    # de un PATCH, por lo que no podemos afirmar estrictamente que 'body' esté en la respuesta,
    # aunque en el "servidor" se mantenga intacto.
    
    print(f"✅ PATCH exitoso: Post {post_id} actualizado parcialmente")

@pytest.mark.api
@pytest.mark.e2e
def test_03_reemplazar_post_completo(post_by_id_url):
    """Valida que se puede reemplazar completamente un post (PUT)."""
    # Usamos un ID existente (1) porque JSONPlaceholder devuelve 404 para PUT en IDs > 100.
    post_id = 1
    url = post_by_id_url(post_id)
    
    full_payload = {
        'id': post_id,
        'title': 'Post completamente reemplazado',
        'body': 'Nuevo contenido completo',
        'userId': 2
    }
    
    response = requests.put(url, json=full_payload)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data['title'] == 'Post completamente reemplazado'
    assert data['body'] == 'Nuevo contenido completo'
    assert data['userId'] == 2
    
    print(f"✅ PUT exitoso: Post {post_id} reemplazado completamente")

@pytest.mark.api
@pytest.mark.e2e
def test_04_eliminar_post(post_by_id_url):
    """Valida que se puede eliminar un post (DELETE)."""
    # Usamos un ID existente (1) para consistencia y fiabilidad en el mock.
    post_id = 1
    url = post_by_id_url(post_id)
    
    response = requests.delete(url)
    
    # JSONPlaceholder devuelve 200 para DELETE (simula eliminación)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    print(f"✅ DELETE exitoso: Post {post_id} eliminado")