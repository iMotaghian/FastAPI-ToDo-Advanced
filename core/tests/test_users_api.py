

def test_login_invalid_data_response_401(anon_client):
    payload = {
        "username":"alibigdeli",
        "password":"a/@1234567"
    }
    response = anon_client.post("/users/login",json=payload)
    assert response.status_code == 401
    
    payload = {
        "username":"testuser",
        "password":"a/@1234567"
    }
    response = anon_client.post("/users/login",json=payload)
    assert response.status_code == 401

    
def test_login_response_200(anon_client):
    payload = {
        "username":"testuser",
        "password":"12345678"
    }
    response = anon_client.post("/users/login",json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    

def test_register_response_201(anon_client):
    payload = {
        "username":"alibigdeli",
        "password":"a/@1234567",
        "password_confirm":"a/@1234567"
    }
    response = anon_client.post("/users/register",json=payload)
    assert response.status_code == 201
    