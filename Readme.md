# Multi-Mission Link Budget


This is a web2py implementation of a satcoms tool to perform link budget analysis.

## Getting Started

**INSTALL WEB2PY:**

```
git clone https://github.com/web2py/web2py.git
cd web2py/scripts
chmod +x setup-web2py-ubuntu.sh //(change for your distribution)
sudo ./setup-web2py-ubuntu.sh
```

**Script also installs:**

* python (2 branch) if it is not present on the machine
* ipython
* postregreSQL 
* apache 2
* python-matplotlib

Edit `modules/config.py` to give the correct propa path

Move this repository to web2py/applications/

Give the directory the correct permissions:

`sudo chown -R www-data:www-data linkbudgetweb`

To install the packages required by linkBudgetWeb, pip command should be available. 
If not, using the following command to install its package:

sudo apt-get install python-pip python-dev build-essential


The CNES propa library file is needed in the web2py user's root
folder (/home/www-data, specified in web2py installation script), which can be found at:
http://10.21.10.14:8081/artifactory/webapp/#/artifacts/browse/tree/General/ext-release-local/fr/cnes/logiciels/20160905.
For the current version, you can download it on Linux:

'cd /home/www-data'
'wget http://10.21.10.14:8081/artifactory/ext-release-local/fr/cnes/logiciels/20160905/propa64.so'

or download it with the web browser directly at:
http://10.21.10.14:8081/artifactory/ext-release-local/fr/cnes/logiciels/20160905/propa64.so
and copy it to the library file's system folder on Windows platform.

To get the latest version of this library file, you need to check out

https://logiciels.cnes.fr/fr/node/32?type=desc

and update to the latest.


### Prerequisites

Multi-Mission Link budget is based on Python 2.7+ and web2py. 

List of prerequisites to be satisfied before start the installation:

* linux machine (ubuntu or centos distribution)
* development profile installed (with gcc included)
* python 2.7+ installed
* sudo privileged 



### Installing



### Running the tests

Explain how to run the automated tests for this system

Break down into end to end tests

Explain what these tests test and why

Give an example
And coding style tests

Explain what these tests test and why

Give an example

### Deployment

Add additional notes about how to deploy this on a live system

### Built With

web2py - The web framework used

### Contributing



### Versioning



### Authors

Damien Roques

Jonathan Karimian

Simon Andersson

### License



### Acknowledgments


Federica Moscato

Alessandro Modigliana