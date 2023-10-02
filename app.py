import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  if test_config is not None:
    setup_db(app,test_config)
  else:
    setup_db(app)
  return app

app = create_app()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.after_request
def after_request(response):
  response.headers.add('Allow-Access-Control-Headers','Content-Type,Authorization')
  response.headers.add('Allow-Access-Control-Methods','GET,POST,PATCH,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response


@app.route('/api/v1/movies',methods=['GET'])
@requires_auth('get:movies')
def get_movies():
  try:
    ##page=request.args.get('page',1,type=int)
    movies=Movie.query.order_by(Movie.id).all()
    ##paginated_questions=paginate(page,10,movies)
    ##categoriesList=Category.query.all()
    return jsonify({
      "success":True,
      "movies": [movie.format() for movie in movies],
      "total_movies":len(movies),
      })
  except:
    abort(404)

@app.route('/api/v1/actors',methods=['GET']) 
@requires_auth('get:actors')
def get_actors():
  try:
    actors=Actor.query.order_by(Actor.id).all()
    return jsonify({
      "success":True,
      "actors": [actor.format() for actor in actors],
      "total_actors":len(actors),
      })
  except:
    abort(404)

@app.route('/api/v1/movies/<int:movie_id>',methods=['DELETE'])
@requires_auth('delete:movie')
def delete_individual_movie(movie_id):
  try:
    movie=Movie.query.get(movie_id)

    if movie is None:
        abort(400)
    
    else:
        movie.delete()
        return jsonify({
            'success':True
        })
  except:
      abort(422)

@app.route('/api/v1/actors/<int:actor_id>',methods=['DELETE'])
@requires_auth('delete:actor')
def delete_individual_actor(actor_id):
  try:
    actor=Actor.query.get(actor_id)

    if actor is None:
        abort(400)
    
    else:
        actor.delete()
        return jsonify({
            'success':True
        })
  except:
      abort(422)


@app.route('/api/v1/movies',methods=['POST']) 
@requires_auth('post:movie')
def create_new_movie():
  body=request.get_json()
  try:
    new_movie=Movie(title=body['title'],release_date=body['release_date'])
    new_movie.insert()
    return jsonify({
              'success':True
          }) 
  except:
    abort(400)

@app.route('/api/v1/actors',methods=['POST']) 
@requires_auth('post:actor')
def create_new_actor():
  body=request.get_json()
  try:
    new_actor=Actor(name=body['name'],age=body['age'],gender=body['gender'])
    new_actor.insert()
    return jsonify({
              'success':True
          }) 
  except:
    abort(400)

@app.route('/api/v1/actors/<int:actor_id>',methods=['PATCH'])
@requires_auth('patch:actor')
def update_individual_actor(actor_id):
  body=request.get_json()
  try:
    actor=Actor.query.get(actor_id)

    if actor is None:
        abort(404)
    
    else:
        if 'name' in body:
          actor.name=body.get('name')
        if 'age' in body:
          actor.age=body.get('age')
        if 'gender' in body:
          actor.gender=body.get('gender')
        actor.update()
        return jsonify({
            'success':True,
            'id':actor.id
        })
  except:
      abort(404)

@app.route('/api/v1/movies/<int:movie_id>',methods=['PATCH'])
@requires_auth('patch:movie')
def update_individual_movie(movie_id):
  body=request.get_json()
  try:
    movie=Movie.query.get(movie_id)

    if movie is None:
        abort(404)
    
    else:
        if 'title' in body:
          movie.title=body.get('title')
        if 'release_date' in body:
          movie.release_date=body.get('release_date')
        movie.update()
        return jsonify({
            'success':True,
            'id':movie.id
        })
  except:
      abort(404)

@app.errorhandler(404)
def not_found(error):
  return jsonify({
      "success":False,
      "error":"Resource not found"
  }),404

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
      "success":False,
      "error":"Unprocessable Entity"
  }),422

@app.errorhandler(400)
def bad_request(error):
  return jsonify({
      "success":False,
      "error":"Bad Request"
  }),400

@app.errorhandler(500)
def server_error(error):
  return jsonify({
      "success":False,
      "error":"Internal Server Error"
  }),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)