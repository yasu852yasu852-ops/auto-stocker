def test_create_and_list_product(client):
    # create
    resp = client.post('/api/products/', json={'sku':'SKU123','name':'Test Product'})
    assert resp.status_code == 201
    # list
    resp = client.get('/api/products/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(p['sku']=='SKU123' for p in data)

def test_duplicate_product(client):
    # create first
    resp = client.post('/api/products/', json={'sku':'DUP1','name':'dup'})
    assert resp.status_code == 201
    # duplicate
    resp = client.post('/api/products/', json={'sku':'DUP1','name':'dup2'})
    assert resp.status_code in (400,409)

def test_delete_product(client):
    resp = client.post('/api/products/', json={'sku':'DEL1','name':'to delete'})
    assert resp.status_code == 201
    resp = client.delete('/api/products/DEL1')
    assert resp.status_code == 200
