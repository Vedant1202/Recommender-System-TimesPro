from app import app
import json
from flask import jsonify
from flask import flash, request
from flask_cors import CORS
from models.recommender_countVectorizer_search import getRecommendationsForSearch
from models.recommender_tfidf_user import getRecommendationsForUser
import pandas as pd


###############################################################################
##                                ROUTES
###############################################################################

CORS(app)

# search recommendations route
@app.route('/recommend/search', methods=['POST'])
# @cross_origin()
def recommendSearch():
    try:
        _query =  request.form.getlist('query')[0]
        # validate the received values
        if _query and request.method == 'POST':
            _results = getRecommendationsForSearch(_query)
            resp = jsonify(results=_results)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        pass


# user recommendations route
@app.route('/recommend/user', methods=['POST'])
# @cross_origin()
def recommendUser():
    try:
        _skills =  request.form.getlist('skills')[0]

        # validate the received values
        if _skills and request.method == 'POST':
            _results = getRecommendationsForUser(_skills)
            resp = jsonify(results=_results)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        pass


# 404 handler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp




if __name__ == "__main__":
    app.run()



#
