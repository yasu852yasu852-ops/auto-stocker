def test_inbound_auto_and_outbound_auto(client, mock_serial):
    # register product
    r = client.post('/api/products/', json={'sku':'FLOW1','name':'Flow Product'})
    assert r.status_code == 201
    # inbound auto
    r = client.post('/api/stock/in/auto', json={'sku':'FLOW1'})
    assert r.status_code == 200
    jr = r.get_json()
    assert jr.get('slot') == 1
    # check state
    r = client.get('/api/stock/state')
    arr = r.get_json()
    assert arr[0]['status'] == 'OCCUPIED'
    assert arr[0]['product'] == 'FLOW1'
    # outbound auto
    r = client.post('/api/stock/out/auto', json={'sku':'FLOW1'})
    assert r.status_code == 200
    jr = r.get_json()
    assert jr.get('slot') == 1
    # check state now empty
    r = client.get('/api/stock/state')
    arr = r.get_json()
    assert arr[0]['status'] == 'EMPTY'
