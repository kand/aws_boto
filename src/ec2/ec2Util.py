from boto.ec2.connection import EC2Connection

VALID_IMGS = {"basicLinuxx32":{"imageid":"ami-76f0061f",
                              "supported_instances":["t1.micro","m1.small","c1.medium"],
                              "username":"root"}}

SECURITY_GROUPS = {"vertex":{"ssh":[22,22,"0.0.0.0/0"],
                             "http":[80,80,"0.0.0.0/0"]
                             }}

class ec2Util(object):
    '''Methods to use aws ec2 instances'''
    
    def __init__(self,aws_access_key,aws_secret_key,region=None):
        '''Default constructor.
        
            Inputs:  
                aws_access_key = access key provided by aws
                aws_secret_key = secret key associated with access key
        '''
        self.__access_key = aws_access_key
        self.__secret_key = aws_secret_key
        self.__region = region
        self.__conn = None
        self.__runningInstances = {}
        
    def open(self):
        '''Creates a new ec2 connection with access and secret key.'''
        self.__conn = EC2Connection(aws_access_key_id = self.__access_key, 
                                    aws_secret_access_key = self.__secret_key)
    def getAvailImages(self):
        '''Get all available images that an ec2 instance can be started up with.'''
        if not self.__checkConn(): return
        return self.__conn.get_all_images()

    def startInstance(self,name,imageName,instanceType,keyPairName):
        '''Start up a new ec2 instance.
        
            Inputs:
                name = name to associate with instance
                imageName = name of image from VALID_IMGS
                instanceType = type of instance to start up, must be in the
                    list for the given VALID_IMGS
                keyPairName = key pair to associate with this image
            Returns: 
                True if instance has successfully started up
        '''
        if not self.__checkConn(): return False
        
        image = self.__conn.get_image(VALID_IMGS[imageName]["imageid"])
        reservation = image.run(instance_type=instanceType,key_name=keyPairName)#,
                                #security_groups=["vertex"])
        instance = reservation.instances[0]
        
        print("Instance starting up...")
        
        instance.update()
        while instance.state != u'running':
            instance.update()
            
        self.__runningInstances[name] = instance
        print("Complete. User = '%s' DNS = '%s'" % (VALID_IMGS[imageName]["username"],instance.dns_name))
        return True
    
    def stopInstance(self,name):
        '''Stop an instance. This does not terminate an instance, however, as boto
            doesn't seem to have a way to do this...
            
            Inputs:
                name = name associated with instance to stop, set when using
                    startInstance()
            Returns:
                True if instance was successfully stopped.
        '''
        if not self.__checkConn(): return False
        if name not in self.__runningInstances.keys():
            print("Name not found in dict of running instances")
            return False
        
        instance = self.__runningInstances[name]
        instance.stop()
        
        print("Instance shutting down...")
        
        instance.update()
        while instance.state != u'stopped':
            print(instance.state)
            instance.update()
            
        self.__runningInstances.pop(name)
        print("Complete.")
        return True

    # this function errors out in boto
    #def close(self):a.close()
    #    '''Close ec2 connection'''
    #    
    #    if not self.__checkConn(): return
    #    self.__conn.close()'''
    #    pass
        
    def __checkConn(self):
        '''Helper function to make sure EC2 connection is open.'''
        if not self.__conn:
            print("[ERROR] must call open() before using this function.")
            return False
        return True
        
if __name__ == "__main__":
    pass
