from tests.base import TestCase
from app.models.user_team import UserTeam


class TestParticipant(TestCase):
    
    def test_create_user_team(self):
        user_team = UserTeam('user', 'team', 1)
        self.assertEqual('user', user_team.user_unid)
        self.assertEqual('team', user_team.team_unid)

    def test_get_user_team(self):
        user_team = UserTeam('user1', 'team1', 1)

        found_user_team = UserTeam.get_user_team('user1', 'team1')
        
        self.assertIsNotNone(found_user_team)
        self.assertEqual(user_team.unid, found_user_team.unid)

