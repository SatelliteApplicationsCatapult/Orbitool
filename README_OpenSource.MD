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


The CNES propa library file, propa64.so for Linux, is needed in the web2py user's root
folder or, propa64.dll for Windows, is needed in the library file's system folder 
(Windows\System32 by default installation) on Windows platform. To get the latest version
of this library file, you need to check out
https://logiciels.cnes.fr/fr/node/32?type=desc



### Prerequisites

Multi-Mission Link budget is based on Python 2.7+ and web2py. 

List of prerequisites to be satisfied before start the installation:

* linux machine (ubuntu or centos distribution)
* development profile installed (with gcc included)
* python 2.7+ installed
* sudo privileged 



### Admin password
The admin password is stored in the files parameters_443.py and parameters_80.py in binary 
format, before accessing to backend GUI and data, you need to reset the admin password with 
the command line command in the web2py's root folder on the Ubuntu platform:
sudo -u www-data python -c "from gluon.main import save_password; save_password('123456',8000)"
sudo cp parameters_8000.py parameters_443.py
sudo cp parameters_8000.py parameters_80.py

### System configuration
1. Cesium key:
in the file [installation folder]\static\js\lbcesium.js, replace the string:
‘your own BingMapsApi key (https://msdn.microsoft.com/en-us/library/ff428642.aspx)’
to your own Cesium key
In the file [installation folder]\views\default\preview.html, replace the string
‘your own BingMapsApi key (https://msdn.microsoft.com/en-us/library/ff428642.aspx)’
to your own Cesium key
2. SMTP server setting:
In the file [installation folder]\models\db.py, the configure email section, you need to
specify your own SMTP server and account to make the login system working.
The current running server in Catapult.org.uk is using the free Google SMTP server: 
	smtp.gmail.com:587
also using a free gmail account as sender "yourusername@gmail.com".
Note that the longin is also required with your email address and password.


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

Jonathan Karimian

Simon Andersson

### License



### Acknowledgments


Federica Moscato

Alessandro Modigliana