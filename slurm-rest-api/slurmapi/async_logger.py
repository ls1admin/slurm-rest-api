import threading
import time
import json
import mysql.connector

from slurmapi import Slurm_Usage
import config

def archive_load(wait_time):
    timer = AsyncTimer()
    timer.wait_time = wait_time
    timer.start()

class AsyncTimer(threading.Thread):
    def run(self):
        while True:
            usage_data = Slurm_Usage().get()

            if 'errors' in usage_data:
                print("usage_data errors: " + str(usage_data))
                print("Error in Usage route, unable to log load data, see error log for more information")
            else:
                usage_data = usage_data['data']

                load_data = {}
                partitions = {}
                for part in usage_data['partitions']:
                    part_data = {}
                    part_data['alloc_cpus'] = usage_data['partitions'][part]['alloc_cpus']
                    part_data['alloc_mem'] = usage_data['partitions'][part]['alloc_mem']
                    part_data['total_mem'] = usage_data['partitions'][part]['real_mem']
                    part_data['total_cpus'] = usage_data['partitions'][part]['total_cpus']
                    part_data['total_nodes'] = usage_data['partitions'][part]['total_nodes']
                    part_data['total_used_cpus_on_active_nodes'] = usage_data['partitions'][part]['total_used_cpus_on_active_nodes']
                    part_data['total_used_mem_on_active_nodes'] = usage_data['partitions'][part]['total_used_mem_on_active_nodes']
                    part_data['partition_load'] = usage_data['partitions'][part]['partition_load']
                    part_data['state'] = usage_data['partitions'][part]['state']
                    partitions[part] = part_data

                load_data['time'] = int(time.time())
                load_data['total_load'] = usage_data['total_load']
                load_data['total_cpus'] = usage_data['total_cpus']
                load_data['total_mem'] = usage_data['total_mem']
                load_data['alloc_cpus'] = usage_data['alloc_cpus']
                load_data['alloc_mem'] = usage_data['alloc_mem']
                load_data['partitions'] = partitions

                # import pdb; pdb.set_trace()
                my_time = load_data['time']
                my_data = json.dumps(load_data)
                sqlc= 'INSERT INTO loadtable (time_id, data_dump) VALUES (%s, %s)'
                valc= (my_time, my_data)

                mysqldb = mysql.connector.connect(
                    host=config.system['mysql_db_host'],
                    user=config.system['mysql_db_user'],
                    passwd=config.system['mysql_db_pass'],
                    database=config.system['mysql_db_name']
                )
                my_cur = mysqldb.cursor()
                my_cur.execute(sqlc, valc)
                mysqldb.commit()

            time.sleep(self.wait_time)

