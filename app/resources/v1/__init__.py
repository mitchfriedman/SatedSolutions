from app.apis import Api
from app.resources.v1.example import Sample
from app.resources.v1.login import Login
from app.resources.v1.register import Register
from app.resources.v1.logout import Logout
from app.resources.v1.team import Teams, Team
from app.resources.v1.teams.participant import Participants, Participant
from app.resources.v1.user import User, Users
from app.resources.v1.invitations import Invitations, Invitation
from app.resources.v1.route import Routes
from app.resources.v1.teams.routes import TeamRoutes


api = Api()

api.add_resource(Sample, '/api/Sample')
api.add_resource(Login, '/api/Login')
api.add_resource(Register, '/api/Register', '/api/Users')
api.add_resource(Logout, '/api/Logout')

api.add_resource(Teams, '/api/Teams')
api.add_resource(Team, '/api/Teams/<string:team_unid>')

api.add_resource(Invitations, '/api/Invitations')
api.add_resource(Invitation, '/api/Invitations/<invitation_unid>')

api.add_resource(Participants, '/api/Teams/<string:team_unid>/Participants')
api.add_resource(Participant, '/api/Teams/<string:team_unid>/Participants/<string:user_unid>')

api.add_resource(Users, '/api/Users')
api.add_resource(User, '/api/Users/<string:user_unid>')


api.add_resource(TeamRoutes, '/api/Teams/<team_unid>/Routes')

api.add_resource(Routes, '/api/Routes')


