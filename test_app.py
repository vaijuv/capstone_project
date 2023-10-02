import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, app
from models import *


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstone"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','Welcome2023','localhost:5432', self.database_name)
        create_app(self.database_path)
        self.client = app.test_client
        #Producer auth token with all permissions
        self.authorization = 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkczMTk2ZElxTnNOcG5VNUZrSWQ1WCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjUxOThjNGM5NzQ1ZDljNjNjMjkxZTI2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2OTYxNzM3OTUsImV4cCI6MTY5NjI2MDE5NSwiYXpwIjoiZk1VVm1PQ1pJVFpUeGhmcVpOSGdNekFWdFVRZjZHc2QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.lcxXxfc2NG6pkwfVAXNUaOi_e7bj1JJNiNxXDEHlL9aUkIxpn5uLWibE5n9_6OgGScRZjgGui2fFagoynUpeaxCtuZ8yGB8aNW_uylxiMBHhhJbrAPxyEctIQ5rT_rH1WGr4kvVY7uhLzZ-m-YemSggHurzGz8FEOwkF6buk8eVdlh-mQo75ZPWLW6ouuhDbFDQFe-nQZ3qacQskz6DYdlwX_yUWBmbkJJt8ErHSdk8lVrh84wIaX43LbYFHGwUdG6j4MVfqFzw7DmlnUSDsKCqIyu-9XMoGthF5UJFhhf_trl0y-QbYEEYcVOumQPpmKbVkVMDESOZ-C8-9iNw-Zg'
        
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    
    
    def test_get_movies(self):
        
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().get('/api/v1/movies',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(data['movies'])

    
    def test_get_movies_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().get('/api/v2/movies',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        
    def test_get_actors(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().get('/api/v1/actors',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors'])

    def test_get_actors_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().get('/api/v2/actors',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_create_new_movie(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().post('/api/v1/movies',json={
            'title':  'Titanic',
            'release_date':  '2023-10-01'
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_create_new_movie_with_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().post('/api/v1/movies',json={
            'title':  'Test Title',
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)

    def test_edit_movie(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().patch('/api/v1/movies/2',json={
            'release_date':  '2023-10-02'
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_edit_movie_with_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().patch('/api/v1/movies/40',json={
            'title':  'Test Title',
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_delete_movies(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().delete('/api/v1/movies/2',headers=headers)
        data=json.loads(res.data)
        with app.app_context():
            movie=Movie.query.get(5)
        self.assertEqual(res.status_code,200)
        self.assertEqual(movie,None)

    def test_delete_movie_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().delete('/api/v1/movies/50',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)

    def test_create_new_actor(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().post('/api/v1/actors',json={
            'name':  'Salman',
            'age':  55,
            'gender':'Male'
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_create_new_actor_with_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().post('/api/v1/actors',json={
            'name':  'Test Name',
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)

    def test_edit_actor(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().patch('/api/v1/actors/2',json={
            'age':  59
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    def test_edit_movie_with_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().patch('/api/v1/actors/40',json={
            'name':  'Test name',
            },headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_delete_actor(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().delete('/api/v1/actors/2',headers=headers)
        data=json.loads(res.data)
        with app.app_context():
            actor=Actor.query.get(6)
        self.assertEqual(res.status_code,200)
        self.assertEqual(actor,None)

    def test_delete_actor_error(self):
        headers = {
            'Authorization': self.authorization
        }
        res=self.client().delete('/api/v1/actors/50',headers=headers)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()