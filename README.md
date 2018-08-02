# Slurm RestAPI

This is a flask based rest interface to slurm.
There are two sub-packages which implement interfaces to different parts of the slurm manager
  * acctapi - interacts with the accounting database slurmdb to get job history and user associations
  * slurmapi - interacts with the pyslurm package to get queue, node, partition, and stat info

Endpoints are
```
/users - can be filtered on user
/history - can be filtered on offset,limit,jobid,user,partition,jobname,associd
/queue
/partitions
/usage - returns additional partition usage information
/nodes
/stats
/load - returns archived load information, `archive_usage_load` must be enabled in config.yml
```

### Configuration

Before setting up the api, you will need to install and run Slurm.

You can setup this api on the machine running slurm, or on an environment that is setup as a sumbit host for your Slurm instance. This can be done by setting up `slurm-drmaa`.

##### Config
Clone this repository, and then modify the `config.yml` file to match your slurmdb credentials and usage needs. Remove the `#` on each line you would like to use and modify their contents, otherwise the system will use the default values which likely will not align to your database.

Note: You may want to create a new user with read-only access for reading from your account database.

The `table_assoc` and `table_job` variables must match the schema names of the assoc and job tables respectively.

### Setup, Install, and Run

Slurm-rest-api is dependant on conda being installed on your system. If you do not already have conda installed you can download miniconda from https://conda.io/miniconda.html

##### Supported versions
Slurm-rest-api has been tested to work on the following versions on slurm and pyslurm:

Slurm version `15.08.4` on pyslurm `15.04.2` using the `override_pyslurm_version_hex` variable with the build script

#### Setup Scripts
The `build.sh` and `run.sh` scripts take care of the environment and dependencies needed for slurm-rest-api

##### Setup
If you are running Slurm `17.11.0` - `17.11.2` you can install by simply running
```
bash build.sh
```

If you are running a different version of slurm, you will need to include the version arguments when running the script.
More details on these arguments can be found by running:
```
bash build.sh --help
```

For a list of slurm versions that are supported by pyslurm, and more information on pyslurm install options, visit https://github.com/PySlurm/pyslurm

##### Building on supported versions

To build on slurm version `15.08.4`run:
```
bash build.sh --pyslurm_version="15.08.2" --override_pyslurm_version_hex="0x0f0804"
```
To build on slurm version `17.02.7` run:
```
bash build.sh --pyslurm_version="17.02.0" --override_pyslurm_version_hex="0x110207"
```
To build on slurm version `17.11.4` run:
```
bash build.sh --pyslurm_version="17.11.0" --override_pyslurm_version_hex="0x110b04"
```

##### Run
To run slurm-rest-api, run:
```
bash run.sh
```

#### Manual Setup
This is an alternative set of setup instructions that can be used to install it manually.

##### Setup

Setup a Conda environment with the needed dependencies inside the clone slurm-rest-api directory:
```
conda create -prefix env python=2.7
source activate env/
conda install mysql cython git
```

Install the version of pyslurm to match your system. The version of pyslurm installed must be compatible with your installed version of slurm or Slurm-rest-api will not install. See https://github.com/PySlurm/pyslurm for more information and a list of supported versions.

Our cluster runs on `slurm 15.08.4` which is unsupported by pyslurm. We can force pyslurm to use this version by editing the setup of `pyslurm 15.08.2`.

```
git clone https://github.com/PySlurm/pyslurm.git
cd pyslurm
git checkout 15.08.2
sed -i 's/__max_slurm_hex_version__ = "0x0f0803"/__max_slurm_hex_version__ = "0x0f0804"/' setup.py
python setup.py build
pip install .
```
pyslurm is now installed on your conda environment.

##### Install and Run

Slurm-rest-api gets installed with pip and then runs locally with network access.

Make sure your conda environment is activated, navigate into the root `slurm-rest-api` directory, and run the following:
```
pip install -e .
export FLASK_APP=slurm-rest-api
flask run --host'0.0.0.0'
```

Note: Installing with `python setup.py build` and `python setup.py install` is not supported.

To verify that Slurm-rest-api is running correctly, enable `serve_index` in `config.yml`, re-run the app, and open your browser to `http://localhost:5000/`. This page will verify that the routes are accessable. Note that some routes may take some time if your database is large.

### Running with NGINX + UWSGI

These instructions were tested to work on Centos7.

If you are using a different version of linux and are not familiar with nginx + uwsgi you will likely be able to find a tutorial that suits your needs by googling "nginx uwsgi flask [linux flavor]".

1: install conda
Download and Install into /opt/miniconda2

2: install epel-release, nginx
```
sudo yum install epel-release nginx
```

3: clone into /opt
```
cd /opt
git clone...
```
Then configure slurm-rest-api and build. Make sure it is working as intended by running locally as described above before moving on.

4: setup user+group permissions

create a new group
add yourself to the group
add username nginx to the group
```
sudo groupadd slurm-rest-api-group
sudo usermod -a -G slurm-rest-api-group username
sudo usermod -a -G slurm-rest-api-group nginx
```

Verify the users have been added to the group
```
grep slurm-rest-api-group /etc/group
```

set slurm-rest-api-group as owner of /opt/slurm-rest-api and /opt/miniconda2
```
sudo chown -R :slurm-rest-api-group /opt/slurm-rest-api
sudo chown -R :slurm-rest-api-group /opt/miniconda2
sudo chmod -R 770 /opt/slurm-rest-api
sudo chmod -R 770 /opt/miniconda2
```
sign out and back in to make sure your group permissions are active

5: modify `/etc/nginx/nginx.conf` to use code block in `sample-block-nginx.conf`

Make sure it matches your install location if you installed it somewhere other than /opt/

6: add `slurm-rest-api.service` to `/etc/systemd/system/`

Make sure it matches your install location if you installed it somewhere other than /opt/

Also make sure the group matches if you used a group name other than slurm-rest-api-group

7: start nginx if not already running
```
sudo systemctl start nginx
```

8: start slurm-rest-api
```
sudo systemctl start slurm-rest-api
```

9: enable both nginx and slurm-rest-api so they start on reboot
```
sudo systemctl enable nginx
sudo systemctl enable slurm-rest-api
```

10: Set SELinux to permissive (if it is enabled).

In `/etc/selinux/config` change `SELINUX=enforcing` to `SELINUX=permissive` to allow slurm-rest-api to connect.

##### Logging
You can uncomment the last line in `slurm-rest-api/slurm-rest-api.ini` to enable uwsgi logging.


### Testing

To run the `unittest` tests activate your conda environment and run:
```
bash tests.sh
```

### Example routes for development

All routes return data in the `JSON` format.

#### Users

| Route | Description |
| --- | --- |
| `http://localhost:5000/users` | All user data |
| `http://localhost:5000/users?name=root` | Returns the user data for a specific user |

#### History

Returns the job history.

`http://localhost:5000/history`

Filters

Multiple filters can be included in a request by seperating them with `&`. See the offset filter for an example of using multiple filters to create history pagination.

| Filter | Comparators | Description | Default | Example |
| --- | --- | --- | --- | --- |
| `limit` | `=` | Number of entries to return | `10` | `http://localhost:5000/history?limit=25` |
| `offset` | `=` | Number of entries to skip, can be used as a "next page" when the number is set to a multiple of the limit parameter | `0` | `http://localhost:5000/history?limit=25&offset=25` |
| `user` | `=` | Only show results from a specific user | N/A | `http://localhost:5000/history?user=galaxy` |
| `partition` | `=` | Only show results from a specific partition | N/A | `http://localhost:5000/history?partition=high` |
| `jobid` | `=`,`>`,`<`,`>=`,`<=` | Only show results with job id matching criteria | N/A |  `http://localhost:5000/history?jobid<=987654` |
| `jobname` | `=` | Only show results with a specific job name | N/A | `http://localhost:5000/history?jobname=g12345_bcftools` |
| `state` | `=` | Only show results with a specific state. See below for state numbers | N/A | `http://localhost:5000/history?state=1` |

State number to type mapping for state filtering

| State Number | State Type |
| --- | --- |
| `0` | `JOB_PENDING` |
| `1` | `JOB_RUNNING` |
| `2` | `JOB_SUSPENDED` |
| `3` | `JOB_COMPLETE` |
| `4` | `JOB_CANCELLED` |
| `5` | `JOB_FAILED` |
| `6` | `JOB_TIMEOUT` |
| `7` | `JOB_NODE_FAIL` |
| `8` | `JOB_PREEMPTED` |
| `9` | `JOB_BOOT_FAIL` |
| `10` | `JOB_DEADLINE` |

#### Queue

Returns the Job Queue

`http://localhost:5000/queue`

#### Partitions

Returns information about all partitions

`http://localhost:5000/partitions`

#### Nodes

Returns information about all nodes

`http://localhost:5000/nodes`

#### Usage

Returns a matrix of data showing all partitions, the nodes on those partitions, and the cpu/memory usage by jobs on each of them.

`http://localhost:5000/usage`

#### Stats

Returns Slurm Statistics

`http://localhost:5000/stats`


#### Load

Returns a list of time stamped load information. When usage load archiving is active, slurm-rest-api will periodically save the current system load, which can then be queried with this route.

| Filter | Comparators | Description | Default | Example |
| --- | --- | --- | --- | --- |
| `time` | `=` | Time period of data to return, measured in seconds (last X seconds) | Same as `archive_wait_time` so a single entry is returned | `http://localhost:5000/load?time=60` |
| `offset` | `=` | Number of seconds to skip, can be used as a "next page" when the number is set to a multiple of the limit parameter | `0` | `http://localhost:5000/load?time=60&offset=120` |


## Front end exampls for the API ##
https://github.com/phac-nml/slurm-rest-api-front


## Legal ##

Copyright Government of Canada 2018

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Contact ##

**Jeffrey Thiessen**: jeffrey.thiessen@canada.ca

**Gary van Domselaar**: gary.vandomselaar@canada.ca

