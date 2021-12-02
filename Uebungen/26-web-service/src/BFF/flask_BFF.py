# for flask see https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
# for flasgger (Swagger) see https://pypi.org/project/flasgger/0.5.4/
import logging,sys
from flask import Flask, jsonify
from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix

from configuration import Configuration
import database_op as db
from grpc_linearregression_client import grpc_linearregression_client
from grpc_gp_client import grpc_gp_client
import dblinreg
import dbgp

DEFAULT_CONFIG = {
    "HOST": "0.0.0.0",
    "PORT": "5000",
    "DEBUG": "False",
    "SERVER": "md2c0gdc"
}

def init_config(args):
    # load configuration
    config=Configuration(DEFAULT_CONFIG)
    config.read_configfiles()
    #This is to add custom args in terminal. They will be added to config then
    config.parse_args(args)
    logging.info('Using config: %s', config.get_config_dict())
    return config

config=init_config(sys.argv[1:])

def create_flask_app(config):
    # ensure that database exists
    if db.create_db(config):
        print('Created database {}.'.format(config['DATABASE']))
    # create flask app
    app=Flask(__name__)
    app.config.update(config.get_dict())
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app

# Create Flask app Instance
app=create_flask_app(config)
print("Flask App instantiated")

Swagger(app)

# UI end points
@app.route("/")
def math_func_intro():
    """Hochschule Karlsruhe, Data Engineering
    ---
    responses:
        200:
            description: Default page
    """
    return "<p>Welcome to mathematical function guessing!</p>"

@app.route("/api/v1/delfitted")
def delete_fitted_functions():
    """Delete all fitted function results
    ---
    responses:
        200:
            description: Deletion of fitted function results completed
    """
    # delete results for linear regression
    lnr=grpc_linearregression_client()
    lnr.delete(config)
    lgp=grpc_gp_client()
    lgp.delete(config)
    return jsonify({"Deletion:","completed"}) # " <p>Deletion of fitted function results completed</p>"

@app.route("/api/v1/guess/<dataset>")
def guess(dataset):
    """Endpoint fits given data points.
    ---
    parameters:
        - name: dataset
          in: path
          type: int
          required: true
    responses:
        200:
            description: returns the state of fitting (scheduling, scheduled, ready)
    """
    d=[]
    # linear regression
    lnr=grpc_linearregression_client()
    state=lnr.run(int(dataset),config)
    d.append({"method":lnr.description,"scheduling":state.scheduling,
        "scheduled":state.scheduled,
        "resultready":state.resultready})
    # genetic programming
    lgp=grpc_gp_client()
    state=lgp.run(int(dataset),config)
    d.append({"method":lgp.description,"scheduling":state.scheduling,
        "scheduled":state.scheduled,
        "resultready":state.resultready})
    return jsonify(d)

@app.route("/api/v1/datasets")
def datasets():
    """Endpoint describes available data sets. Information is retrieved from database.
    ---
    responses:
        200:
            description: Information about available data sets.
    """
    functions=db.get_functions_db(config)
    d=[]
    for f in functions:
        d.append({"id": f.id, "name": f.name, "description":f.description })
    return jsonify(d)

@app.route("/api/v1/fittedfunction")
def fittedfunction():
    """Endpoint retrieves fitted functions for all available data sets.
    ---
    responses:
        200:
            description: Information about fitted functions.
    """
    # get information from linear regression
    fnc,rmse=dblinreg.get_functions(config)
    d=[]
    for f in zip(fnc,rmse):
        d.append({"Method": "linear regression", "Function": f[0], "RMSE": f[1] })
    # get information from genetic programming
    fgp,rmse=dbgp.get_functions(config)
    for f in zip(fgp,rmse):
        d.append({"Method": "genetic programming", "Function": f[0], "RMSE": f[1]})
    return jsonify(d)

if __name__ == "__main__":
    config=app.config
    app.run(host=config['HOST'],
            port=int(config['PORT']),
            debug=(config['DEBUG'] == 'True'),
            threaded=True)