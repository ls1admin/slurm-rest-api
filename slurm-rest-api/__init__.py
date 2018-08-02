from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from acctapi import db_session, init_db, JobHistoryApi, UserAssocApi
from slurmapi import Slurm_Queue, Slurm_Statistics, Slurm_Nodes, Slurm_Partitions, Slurm_Usage, Slurm_Load, archive_load
from tinydb import TinyDB
import config

application = Flask(__name__)
application.debug = config.system['debug']

if config.system['use_cors']:
    CORS(application)

api = Api(application)

if config.system['use_acct_db']:
    @application.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    init_db()

    api.add_resource(JobHistoryApi, '/history')
    api.add_resource(UserAssocApi, '/users')

api.add_resource(Slurm_Queue, '/queue')
api.add_resource(Slurm_Nodes, '/nodes')
api.add_resource(Slurm_Partitions, '/partitions')
api.add_resource(Slurm_Statistics, '/stats')
api.add_resource(Slurm_Usage, '/usage')

if config.system['archive_usage_load']:
    api.add_resource(Slurm_Load, '/load')
    db = TinyDB(config.system['archive_path'])
    archive_load(db, config.system['archive_wait_time'])

# we can serve a webpage straight from flask, this should only be used for developing.
if config.system['serve_index']:
    from flask import send_from_directory
    @application.route('/')
    def static_index():
        return send_from_directory('','static/index.html')

if __name__ == '__main__':
    application.run()
