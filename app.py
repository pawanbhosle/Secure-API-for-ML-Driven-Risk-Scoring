from flask import Flask, request, jsonify, Blueprint
from flask_restplus import Api, Resource, fields, Namespace
import os
from tasks import compute_risk_score_task


app = Flask(__name__)
API_KEY = "authorization_token"


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-API-KEY')
        print('token', token)
        if not token or token != API_KEY:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return wrapper


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
api = Api(blueprint,
          title="Secure Risk Scoring API",
          version='1.0',
          description='API for computing ML risk scores',
          authorizations=authorizations,
          )


risk_ns = Namespace('risk-score', description='Risk scoring operations', authorizations=authorizations)
api.add_namespace(risk_ns, path='/api/v1/risk-score')

model = risk_ns.model('RiskInput', {
    'purpose': fields.String(required=True),
    'data_sensitivity': fields.String(required=True),
    'region': fields.String(required=True),
    'processor': fields.String(required=True)
})


@risk_ns.route('/')
class RiskScorer(Resource):
    @risk_ns.expect(model)
    @risk_ns.doc(security='apikey')
    @token_required
    def post(self):
        data = request.json
        task = compute_risk_score_task(data)
        print(task)
        return {"task_id": task, "message": "Risk score computation in progress"}, 202


app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)
