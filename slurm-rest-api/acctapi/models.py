from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import config

class Assoc(Base):
    __tablename__ = config.database['table_assoc']
    id_assoc = Column('id_assoc', Integer, primary_key=True)
    user = Column('user', String)
    acct = Column('acct', String)
    partition = Column('partition', String)

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self):
        me = dict()
        me['id_assoc']=int(self.id_assoc)
        me['user']= self.user
        me['acct']= self.acct
        me['partition']= self.partition
        return me

class Job(Base):
    __tablename__ = config.database['table_job']
    # job_db_inx =  Column('job_db_inx', Integer, primary_key=True)
    # mod_time = Column('mod_time', Integer)
    # deleted = Column('deleted', Integer)
    account = Column('account', String)
    # admin_comment = Column('admin_comment', String)
    # array_task_str = Column('array_task_str', String)
    # array_max_tasks = Column('array_max_tasks', Integer)
    # array_task_pending = Column('array_task_pending', Integer)
    cpus_req = Column('cpus_req', Integer)
    # derived_ec = Column('derived_ec', Integer)
    # derived_es = Column('derived_es', String)
    # exit_code = Column('exit_code', Integer)
    job_name  = Column('job_name', String)
    id_assoc  = Column('id_assoc', Integer)
    # id_array_job  = Column('id_array_job', Integer)
    # id_array_task = Column('id_array_task', Integer)
    # id_block = Column('id_block', String)
    id_job = Column('id_job', Integer)
    # id_qos = Column('id_qos', Integer)
    # id_resv = Column('id_resv', Integer)
    # id_wckey = Column('id_wckey', Integer)
    id_user = Column('id_user', Integer)
    # id_group = Column('id_group', Integer)
    # pack_job_id = Column('pack_job_id', Integer)
    # pack_job_offset = Column('pack_job_offset', Integer)
    # kill_requid = Column('kill_requid', Integer)
    # mcs_label = Column('mcs_label', String)
    mem_req = Column('mem_req', Integer)
    nodelist = Column('nodelist', String)
    nodes_alloc = Column('nodes_alloc', Integer)
    # node_inx = Column('node_inx', String)
    partition = Column('partition', String)
    priority = Column('priority', Integer)
    state = Column('state', Integer)
    timelimit = Column('timelimit', Integer)
    time_submit = Column('time_submit', Integer)
    # time_eligible = Column('time_eligible', Integer)
    time_start = Column('time_start', Integer)
    time_end = Column('time_end', Integer)
    # time_suspended = Column('time_suspended', Integer)
    # gres_req = Column('gres_req', String)
    # gres_alloc = Column('gres_alloc', String)
    # gres_used = Column('gres_used', String)
    # wckey = Column('wckey', String)
    # work_dir = Column('work_dir', String)
    # system_comment = Column('system_comment', String)
    # track_steps = Column('track_steps', Integer)
    # tres_alloc = Column('tres_alloc', String)
    # tres_req = Column('tres_req', String)

    def __repr__(self):
        return str(self.to_dict())

    def conv_timestamp(self,time):
        rval =""
        if time>0:
            rval = datetime.fromtimestamp(time).ctime()
        return rval

    def conv_timelimit(self, minutes):
        hours, mins = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return "%dd:%dh:%dm" %(days,hours,mins)

    def to_dict(self):
        states = [
          'JOB_PENDING',
          'JOB_RUNNING',
          'JOB_SUSPENDED',
          'JOB_COMPLETE',
          'JOB_CANCELLED',
          'JOB_FAILED',
          'JOB_TIMEOUT',
          'JOB_NODE_FAIL',
          'JOB_PREEMPTED',
          'JOB_BOOT_FAIL',
          'JOB_DEADLINE'
        ]
        me = dict()
        me['id_job']=int(self.id_job)
        me['id_user']= int(self.id_user)
        me['id_assoc']= int(self.id_assoc)
        me['job_name']= self.job_name
        me['cpus_req']= int(self.cpus_req)
        me['mem_req']= int(self.mem_req)
        me['account']= self.account
        me['nodelist']= self.nodelist
        me['partition']= self.partition
        me['nodes_alloc']= int(self.nodes_alloc)
        me['timelimit']=self.conv_timelimit(int(self.timelimit))
        me['time_submit']=self.conv_timestamp(int(self.time_submit))
        me['time_start']=self.conv_timestamp(int(self.time_start))
        me['time_end']=self.conv_timestamp(int(self.time_end))
        me['priority']=int(self.priority)
        self.state= max(min(10, int(self.state)),0)
        me['state'] = states[self.state]
        return me
