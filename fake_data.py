from app.database import stub


def import_data():
    stub()
    create_users()


def create_users():
    from app.models.user import User
    User('cfc-user1@mail.com', 'a', 'first', 'last', True)


if __name__ == '__main__':
    import_data()

