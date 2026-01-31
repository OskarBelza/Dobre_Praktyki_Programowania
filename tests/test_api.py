from fastapi import status


def test_login_success(client, regular_user):
    """Sprawdza poprawne logowanie."""
    response = client.post("/login", json={
        "email": regular_user["email"],
        "password": regular_user["password"]
    })

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(client, regular_user):
    """Sprawdza błędne hasło."""
    response = client.post("/login", json={
        "email": regular_user["email"],
        "password": "WRONG_PASSWORD"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Niepoprawny email lub hasło"


def test_login_non_existent_user(client):
    """Sprawdza logowanie kontem, które nie istnieje."""
    response = client.post("/login", json={
        "email": "ghost@test.pl",
        "password": "whatever"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_user_as_admin(client, admin_user):
    """Admin powinien móc dodać nowego użytkownika."""
    # 1. Zaloguj się jako admin, by zdobyć token
    login_res = client.post("/login", json=admin_user)
    token = login_res.json()["access_token"]

    # 2. Wyślij żądanie utworzenia użytkownika
    new_user_data = {
        "email": "new_guy@test.pl",
        "password": "secret_pass",
        "roles": "ROLE_USER"
    }

    response = client.post(
        "/users",
        json=new_user_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "Użytkownik new_guy@test.pl utworzony" in response.json()["message"]


def test_create_user_as_regular_user_forbidden(client, regular_user):
    """Zwykły user NIE powinien móc dodać użytkownika (Brak ROLE_ADMIN)."""
    # 1. Zaloguj się jako zwykły user
    login_res = client.post("/login", json=regular_user)
    token = login_res.json()["access_token"]

    # 2. Próba utworzenia użytkownika
    response = client.post(
        "/users",
        json={"email": "hacker@test.pl", "password": "123"},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Oczekujemy 403 Forbidden
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Brak uprawnień" in response.json()["detail"]


def test_create_user_no_token(client):
    """Bez tokena nie można dodać użytkownika."""
    response = client.post(
        "/users",
        json={"email": "ghost@test.pl", "password": "123"}
    )
    # Oczekujemy 401 Unauthorized (niezalogowany)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_details_success(client, regular_user):
    """Zalogowany użytkownik może zobaczyć swoje detale."""
    # 1. Login
    login_res = client.post("/login", json=regular_user)
    token = login_res.json()["access_token"]

    # 2. Pobranie detali
    response = client.get(
        "/user_details",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "ROLE_USER" in data["roles"]
    assert isinstance(data["user_id"], int)


def test_user_details_no_token(client):
    """Brak tokena blokuje dostęp."""
    response = client.get("/user_details")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
