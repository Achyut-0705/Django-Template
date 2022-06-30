from django.test import TestCase
from rest_framework.authtoken.models import Token
from .models import *
from Accounts.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APIClient, APIRequestFactory, APITestCase, URLPatternsTestCase
# Create your tests here.


class AssetTests(APITestCase):
    def test_create(self):
        user = CustomUser.objects.create(username="abc", address="lcna", mobile_no="9811132747", role="Admin",
                                         first_name="sid", last_name="sar")
        user.set_password('s')
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(reverse('asset-list'),
                    data={"name":"DabApps", "longitude":0, "latitude":0, "address":"aa"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(College.objects.count(), 1)
        self.assertEqual(College.objects.get().name, 'DabApps')
        response = client.get("http://127.0.0.1:8000/api/asset/detail/1",
                                follow=True)
        self.assertEqual(response.data.get('name'), 'DabApps')
        # self.client.login(username="abc",password="s", token=token)
        # response = self.client.post(url, {'name': 'DabApps', 'longitude': 0, 'latitude': 0})
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Asset.objects.count(), 1)
        # self.assertEqual(Asset.objects.get().name, 'DabApps')


    # def test_retreival(self):
    #     user = CustomUser.objects.create(username="abc", address="lcna", mobile_no="9811132747", role="Admin",
    #                                      first_name="sid", last_name="sar")
    #     user.set_password('s')
    #     token = Token.objects.create(user=user)
    #     url = reverse('asset-detail', kwargs={'id':1})
    #     client = APIClient()
    #     client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #     response = client.get(url, follow=True)
    #     self.assertEqual(response.data.get('name'), 'DabApps')

    # # def test_update(self):
    # #     url = reverse('asset-detail', kwargs={'id': 1})
    # #     data = {'name':'s'}
    # #     response = self.client.patch(url, data, format='json')
    # #     self.assertEqual(response.name, 's')



class InspectionTests(APITestCase):     
    def test_inspection(self):    
        asset = College.objects.create(name="s", latitude=0, longitude=0)
        user = CustomUser.objects.create(username="abc", address="lcna", mobile_no="9811132747", role="Admin",
                                         first_name="sid", last_name="sar")
        user.set_password('s')
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        print({"made_by": user.id, "assigned_to": user.id,
              "district": "mc", "branch": "aa", "quality": "ok", "assets": [1]})
        response = client.post('http://127.0.0.1:8000/api/inspection/list/', 
                                data={"made_by":user.id, "assigned_to":user.id, "district":"mc", "branch":"aa", "quality":"ok", "assets":[1]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = client.get("http://127.0.0.1:8000/api/inspection/detail/1",
                              follow=True)
        self.assertEqual(response.data.assets.count(), 1)


# class InspectionTestCase(TestCase):
#     def setUp(self):
#         asset = Asset.objects.create(name="s", latitude=0, longitude=0)
#         user = CustomUser.objects.create(username="abc", address="lcna", mobile_no="9811132747", role="Admin", 
#                                          first_name="sid", last_name="sar")
#         inspection = Inspection.objects.create(made_by=user, assigned_to=user, district="mc", branch="aa", quality="ok", status="Approved")
#         inspection.assets.add(asset)
#         inspection.save()


#     def test_values(self):
#         inspection = Inspection.objects.get()
#         user = CustomUser.objects.get()
#         asset = Asset.objects.get()
#         self.assertEqual(inspection.made_by, user)
#         self.assertEqual(inspection.assigned_to, user)
#         self.assertEqual(inspection.assets.filter().first(), asset)
