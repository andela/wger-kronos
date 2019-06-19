from wger.core.tests.base_testcase import WorkoutManagerTestCase
from django.core.urlresolvers import reverse_lazy


class GymListTest(WorkoutManagerTestCase):
    '''
    test gym member list
    '''

    def test_user_list_returned(self):
        self.user_login()

        members_url = reverse_lazy('gym:gym:user-list', kwargs={'pk': 1})
        response = self.client.get(members_url)

        self.assertEqual(response.context['active_user_count'], 9)
        self.assertEqual(response.context['deactivated_user_count'], 1)
        self.assertEqual(response.context['admin_count'], 7)
