'''
Created on Feb 17, 2011

@author: kos
'''

from boto.ec2 import regions
from boto.ec2.connection import EC2Connection

class util(object):
    '''Methods to start up/manage/terminate ec2 instances'''
    
    __ERROR_START_CONN = "[ERROR] Please call open() to open an EC2 connection before attempting to call this function."

    def __init__(self,aws_access_key,aws_secret_key,region=regions()[1]):
        self.__access_key = aws_access_key
        self.__secret_key = aws_secret_key
        self.__region = region
        self.__conn = None;
        
    def open(self):
        '''Creates a new ec2 connection with access and secret key in specified
        region. Connects to us-east by default.'''
        self.__conn = EC2Connection(aws_access_key_id = self.__access_key, 
                                    aws_secret_access_key = self.__secret_key,
                                    region = self.__region)
    @_checkConn
    def getAvailImages(self):
        pass

    @_checkConn
    def startInstance(self):
        pass

    @_checkConn
    def closeConn(self):
        '''Close ec2 connection'''
        self.__conn.close()
        
    
def _checkConn(f):
    '''Function decorator to check if connection is open.'''
    def wrap(self,*args,**kwargs):
        if not self.__conn:
            print(self.__ERROR_START_CONN)
        else:
            return f(self,*args,**kwargs)
        
    return wrap
        
if __name__ == "__main__":
    pass