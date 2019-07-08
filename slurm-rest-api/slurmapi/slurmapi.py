from flask_restful import Resource, reqparse
from tinydb import TinyDB, Query
import config
import pyslurm
import pwd
import re
import json
import time
import mysql.connector


import filter_slurm
from parse_slurm_node_list import parse_all_lists, parse_list

class Slurm_Queue(Resource):
    def get(self):
        json_data = {}
        try:
            j = pyslurm.job()
            data = j.get()
            for id,job in data.iteritems():
                job['user_name'] = pwd.getpwuid(job['user_id'])[0]
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

class Slurm_Statistics(Resource):
    def get(self):
        json_data = {}
        try:
            s = pyslurm.statistics()
            data = s.get()
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

class Slurm_Nodes(Resource):
    def get(self):
        json_data = {}
        try:
            n = pyslurm.node()
            data = n.get()
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

class Slurm_Partitions(Resource):
    def get(self):
        json_data = {}
        try:
            p = pyslurm.partition()
            data = p.get()
            filter_slurm.filter_partitions(data, config.filter['partitions'])
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

class Slurm_Load(Resource):

    def get(self):
        json_data = {}
        try:
            data = self._get_load()
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)

        return json_data

    def _get_load(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time', type=int, default=config.system['archive_wait_time'])
        parser.add_argument('offset', type=int, default=0)
        args = parser.parse_args()

        now = int(time.time())
        q_start_time = now - args['time'] - args['offset']
        q_end_time = now - args['offset']

        mysqldb = mysql.connector.connect(
            host=config.system['mysql_db_host'],
            user=config.system['mysql_db_user'],
            passwd=config.system['mysql_db_pass'],
            database=config.system['mysql_db_name'])
        my_cur = mysqldb.cursor()
        sqlc = "select data_dump from loadtable where time_id >= {} && time_id <= {}".format(q_start_time, q_end_time)
        my_cur.execute(sqlc)
        res = my_cur.fetchall()

        my_data = []
        for x in res:
            my_data.append(json.loads(x[0]))

        return my_data

class Slurm_Usage(Resource):
    def get(self):
        json_data = {}
        try:
            p = pyslurm.partition()
            p_data = p.get()
            filter_slurm.filter_partitions(p_data, config.filter['partitions'])
            n = pyslurm.node()
            n_data = n.get()
            j = pyslurm.job()
            j_data = j.get()
            data = self._get_usage(p_data, n_data, j_data)
            json_data["data"] = data
        except Exception as e:
            error = {
                "title" : "Python Exception",
                "meta" : {"args" : e.args}
            }
            json_data["errors"] = [error]
            print("Error: " + self.__str__() + " : " + e.message)
            print("error message" + str(e.args))

        return json_data

    def _get_usage(self, p_data, n_data, j_data):
        # Create full_node_list which is the list of all active nodes
        all_partitions_node_lists = []
        for part in p_data:
            all_partitions_node_lists.append(p_data[part]['nodes'])
        full_node_list = parse_all_lists(all_partitions_node_lists)

        u_data = {}
        part_data = {}
        for part in p_data:
            part_data[part] = {}
            part_data[part]['total_nodes'] = p_data[part]['total_nodes']
            part_data[part]['nodes'] = {}
            
            # create a list of all nodes on this partition and set active to false, later we will set teh ones being used to true
            for x in full_node_list:
                part_data[part]['nodes'][x] = {}
                part_data[part]['nodes'][x]['active'] = False

            part_data[part]['state'] = p_data[part]['state']
            part_data[part]['total_cpus'] = p_data[part]['total_cpus']
            # Verify priority exists before using it, this may be slurm version dependant
            # TODO: In the future we might want this to be decided based off the version of slurm that is being used.
            if 'priority' in p_data[part]:
                part_data[part]['priority'] = p_data[part]['priority']
            elif 'priority_tier' in p_data[part]:
                part_data[part]['priority'] = p_data[part]['priority_tier']

            # Get list of all nodes in use
            nodes_str = p_data[part]['nodes']
            active_nodes = parse_list(nodes_str)

            real_mem = 0
            total_cpus_used_on_available_nodes = 0
            total_mem_used_on_available_nodes = 0
            for a in active_nodes:
                node = n_data[a]
                real_mem = real_mem + node['real_memory']
                total_cpus_used_on_available_nodes += node['alloc_cpus']
                total_mem_used_on_available_nodes += node['alloc_mem']

                part_data[part]['nodes'][a]['active'] = True
                part_data[part]['nodes'][a]['total_used_cpus'] = node['alloc_cpus']
                part_data[part]['nodes'][a]['total_used_mem'] = node['alloc_mem']
                part_data[part]['nodes'][a]['total_cpus'] = node['cpus']
                part_data[part]['nodes'][a]['total_memory'] = node['real_memory']
                part_data[part]['nodes'][a]['cpus_allocated'] = 0
                part_data[part]['nodes'][a]['mem_allocated'] = 0
                part_data[part]['nodes'][a]['running_jobs'] = 0
            part_data[part]['real_mem'] = real_mem
            part_data[part]['total_used_cpus_on_active_nodes'] = total_cpus_used_on_available_nodes
            part_data[part]['total_used_mem_on_active_nodes'] = total_mem_used_on_available_nodes

        for job in j_data:
            if j_data[job]['job_state'] in ['RUNNING', 'SUSPENDED']:  
                part = j_data[job]['partition']
                for c in j_data[job]['cpus_allocated']:
                    if c in part_data[part]['nodes']:
                        if 'cpus_allocated' not in part_data[part]['nodes'][c]:
                            part_data[part]['nodes'][c]['cpus_allocated'] = 0
                        if 'mem_allocated' not in part_data[part]['nodes'][c]:
                            part_data[part]['nodes'][c]['mem_allocated'] = 0
                        if 'running_jobs' not in part_data[part]['nodes'][c]:
                            part_data[part]['nodes'][c]['running_jobs'] = 0
                        part_data[part]['nodes'][c]['cpus_allocated'] = part_data[part]['nodes'][c]['cpus_allocated'] + j_data[job]['cpus_allocated'][c]
                        if j_data[job]['min_memory_node']:
                            part_data[part]['nodes'][c]['mem_allocated'] = part_data[part]['nodes'][c]['mem_allocated'] + j_data[job]['min_memory_node']
                        part_data[part]['nodes'][c]['running_jobs'] = part_data[part]['nodes'][c]['running_jobs'] + 1

        for part in p_data:
            nodes_str = p_data[part]['nodes']
            active_nodes = parse_list(nodes_str)
            load_this_partition = 0.0
            used_cpus = 0
            used_mem = 0
            for a in active_nodes:
                load_cpu = float(part_data[part]['nodes'][a]['cpus_allocated']) / float(part_data[part]['nodes'][a]['total_cpus'])
                load_mem = float(part_data[part]['nodes'][a]['mem_allocated']) / float(part_data[part]['nodes'][a]['total_memory'])

                used_cpus += part_data[part]['nodes'][a]['cpus_allocated']
                used_mem += part_data[part]['nodes'][a]['mem_allocated']
                if load_cpu > load_mem:
                    load_this_partition += load_cpu
                else:
                    load_this_partition += load_mem
            load_this_partition = load_this_partition / float(p_data[part]['total_nodes'])
            part_data[part]['partition_load'] = load_this_partition
            part_data[part]['alloc_cpus'] = used_cpus
            part_data[part]['alloc_mem'] = used_mem

        u_data['partitions'] = part_data

        total_load = 0.0
        used_cpus = 0
        used_mem = 0
        total_cpus = 0
        total_mem = 0
        for n in n_data:
            load_cpu = float(n_data[n]['alloc_cpus']) / float(n_data[n]['cpus'])
            load_mem = float(n_data[n]['alloc_mem']) / float(n_data[n]['real_memory'])

            used_cpus += n_data[n]['alloc_cpus']
            used_mem += n_data[n]['alloc_mem']
            total_cpus += n_data[n]['cpus']
            total_mem += n_data[n]['real_memory']
            if load_cpu > load_mem:
                total_load += load_cpu
            else:
                total_load += load_mem
        total_load = total_load / float(len(n_data))
        u_data['total_load'] = total_load
        u_data['alloc_cpus'] = used_cpus
        u_data['alloc_mem'] = used_mem
        u_data['total_cpus'] = total_cpus
        u_data['total_mem'] = total_mem

        return u_data
