FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$9WuKLJs8AbkHcyiVqXl2oOy31byfae3hJu1HlbSgSAyWwjczEK/hm",
        "role": "admin",
    },
    "employe": {
        "username": "employe",
        "hashed_password": "$2b$12$bxD4VIkp13G0iXI5.gk5guMMRYHUMyAotF1o/ixipNAFKpQhJhRSy",
        "role": "employee",
    },
}


def get_user(username: str) -> dict | None:
    return FAKE_USERS_DB.get(username)