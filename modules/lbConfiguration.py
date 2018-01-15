import platform
if platform.system() == 'Windows':
    pathtopropa = 'C:\\Windows\\SysWOW64\\propa.dll'
elif platform.system() == 'Linux':
    pathtopropa = "/home/www-data/web2py/applications/linkbudgetweb/propa64.so"
