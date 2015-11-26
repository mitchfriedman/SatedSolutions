from app.apis import Api
from app.resources.v1.example import Sample
from app.resources.v1.login import Login
from app.resources.v1.register import Register
from app.resources.v1.logout import Logout
from app.resources.v1.team import Teams, Team
from app.resources.v1.teams.participant import Participants


api = Api()


api.add_resource(Sample, '/api/Sample')
api.add_resource(Login, '/api/Login')
api.add_resource(Register, '/api/Register')
api.add_resource(Logout, '/api/Logout')

api.add_resource(Teams, '/api/Teams')
api.add_resource(Team, '/api/Team/<string:team_unid>')

api.add_resource(Participants, '/api/Team/<string:team_unid>/Participants')

