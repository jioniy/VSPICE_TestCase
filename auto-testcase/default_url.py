# -*- coding: utf-8 -*-
import socket

# 가상화서버 내에서는 아이피 대역이 다름. 
# 따라서 Jenkins에서 수행할 때는 가상화 환경 내의 IP로 설정해서 사용
# 이 파일은 수정은 하되, 커밋하지 말 것

VSPICE_URL = ''
# SVN_URL = ''

myip = socket.gethostbyname_ex(socket.gethostname())

if '192.168.0.' in str(myip) :
    VSPICE_URL = 'http://192.168.0.130:9050/vspice/'
    # SVN_URL = 'https://192.168.0.130:8443/svn/'
else :
    VSPICE_URL = 'http://192.168.122.67:18080/vspice/'
    # SVN_URL = 'https://test-PC:8443/svn/'