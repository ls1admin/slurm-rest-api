from flask_restful import Resource, Api, reqparse
from models import Job, Assoc
from sqlalchemy import desc


class UserAssocApi(Resource):
    def get(self):
        json_data = {}
        try:
            data = self._get_users()
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

    def _get_users(self):
        parser =reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        if args['name']:
            userlist = Assoc.query.filter(Assoc.user == args['name']).all()
        else:
            userlist = Assoc.query.filter(Assoc.user != "").all()
        ul = list()
        for user in userlist:
            ul.append(user.to_dict())

        return ul

class JobHistoryApi(Resource):

    def get(self):
        json_data = {}
        try:
            data = self._get_history()
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

    def _get_history(self):
        parser =reqparse.RequestParser()
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('offset', type=int, default=0)
        parser.add_argument('user')
        parser.add_argument('associd', type=int, default=None)
        parser.add_argument('state', type=int, default=None)
        parser.add_argument('startbefore')
        parser.add_argument('startafter')
        parser.add_argument('endafter')
        parser.add_argument('endbefore')
        parser.add_argument('jobname')
        parser.add_argument('partition')
        parser.add_argument('jobid', type=int)
        args = parser.parse_args()
        criterion = list()

        if args['user']:
            userlist = Assoc.query.filter(Assoc.user==args['user']).all()
            id_list = list()
            for assoc in userlist:
                id_list.append(assoc.id_assoc)
            criterion.append(Job.id_assoc.in_(id_list))
        if args['associd']:
            criterion.append(Job.id_assoc==args['associd'])
        if args['jobname']:
            criterion.append(Job.job_name==args['jobname'])
        if args['jobid']:
            criterion.append(Job.id_job==args['jobid'])
        if args['partition']:
            criterion.append(Job.partition==args['partition'])
        if args['state']:
            criterion.append(Job.state==args['state'])

        userlist = Assoc.query.all()
        joblist = Job.query.filter(*criterion).order_by(desc(Job.time_submit)).limit(args['limit']).offset(args['offset']).all()

        users = dict()
        for user in userlist:
            users[user.id_assoc]=user.user
        rlist = list()
        for job in joblist:
            jd = job.to_dict()
            jd['user_name'] = users.get(jd['id_assoc'], "")
            rlist.append(jd)

        return rlist
