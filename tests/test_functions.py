def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200

def test_register_account(test_client, init_database):
    payload= """{
        "username": "testdddUsername",
        "email": "test@test.test",
        "password": "testPassword",
        "role": "admin"
    }"""
    response = test_client.post('/api/register', data=payload)
    json_res = response.get_json()

    assert response.status_code == 200
    assert json_res['message'] == "user has been created"



def test_login_account(test_client, init_database):
    payload= """{
        "email": "test1@test.com",
        "password": "password1"
    }"""
    response = test_client.post('/api/login', data=payload)
    json_res = response.get_json()
    assert response.status_code == 200
    assert json_res['token'] != None


def test_get_restaurants(test_client, init_database):
    response = test_client.get('/api/restaurant')
    json_res = response.get_json()
    assert response.status_code == 200
    assert len(json_res['message']) >= 0


def test_get_restaurant_menu(test_client, init_database):
    response = test_client.get('/api/restaurant/1/menu')
    json_res = response.get_json()
    assert response.status_code == 200
    assert len(json_res['message']) >= 0


def test_post_order(test_client, init_database, get_token):
    jwt = get_token
    response = test_client.post('/api/restaurant/1/order', headers={"x-access-tokens": jwt})
    json_res = response.get_json()
    assert response.status_code == 200
    assert json_res['message'] == 'order has been created'


def test_post_orderItem(test_client, init_database, get_token):
    jwt = get_token
    payload= """{
        "quantity": 55
    }"""
    response = test_client.post('/api/restaurant/1/order/1/item/1', data=payload, headers={"x-access-tokens": jwt})
    json_res = response.get_json()
    print(response)
    assert response.status_code == 200
    assert json_res['message'] == 'item has been added!'


# NOTE
# We have to handle all cases for each route like giving wrong 
# json body or invalid token to see the API behavior in all cases