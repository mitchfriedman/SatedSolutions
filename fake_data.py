from app.database import stub


def import_data():
    stub()
    create_users()
    create_routes()


def create_users():
    from app.models.user import User
    User('cfc-user1@mail.com', 'a', 'first', 'last', True)

def create_routes():
    from app.models.route import Route
    Route('Route 1', 'university of guelph, ontario', 'cherry blossom guelph, ontario', '5:30', 'Bus', 'No')
    Route('Awesome Route 241', 'Stone Road Mall, Ontario', 'Popeyes Guelph, Ontario', '7:30', 'Walking', 'Yes')
    Route('My CFC route', 'Stone Road Mall, Ontario', 'Stone Road Mall, Ontario', '7:30', 'Driving', 'No')


if __name__ == '__main__':
    import_data()

