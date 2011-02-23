from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message    

#Note: custom message classes can be created if they are a subclass of
#    the boto.sqs.message.Message class, then on a queue, the Message class
#    can be set using q.set_message_class(<custom message class>)

class sqsUtil(object):
    '''Methods to use aws sqs'''

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
        
    def open(self):
        '''Creates a new sqs connection with given access and secret key.'''
        self.__conn = SQSConnection(aws_access_key_id = self.__access_key,
                                    aws_secret_access_key = self.__secret_key)
        
    def createQueue(self,name,visibilityTimeout=30):
        '''Creates a new queue.
        
            Input:
                name = name to associate with queue
                visibilityTimeout = how long, in seconds, to hide a message
                    before it can be read again.
            
            Returns:
                True if queue was successfully created.
        '''
        if not self.__checkConn(): return False
        
        self.__conn.create_queue(name,visibilityTimeout)
        return True
    
    def getVisibilityTimeout(self,name):
        '''Get visibility time out of a queue.
        
            Inputs:
                name = name of queue
        '''
        if not self.__checkConn(): return False

    def getQueue(self,name):
        '''Get a queue.
            
            Inputs:
                name = name of queue
            
            Returns:
                A queue object or None if queue object not found
        '''
        if not self.__checkConn(): return None
        return self.__conn.get_queue(name)
    
    def getAllQueues(self,prefix=""):
        '''Get a list of all queues created.
            
            Inputs:
                prefix = restricts return to names that start with prefix
                
            Returns:
                A ResultSet object of queues. Calling id on one of these queues
                    will get the id of the queue.
        '''
        if not self.__checkConn(): return None
        return self.__conn.get_all_queues(prefix)
    
    def writeToQueue(self,name,message,messageClass=None):
        '''Write a message to a queue.
        
            Inputs:
                name = name of queue to write to
                message = message to write into queue
                messageClass = a custom message class to use to write into queue
            
            Returns:
                False if message was not written, true otherwise
        '''
        if not self.__checkConn(): return False
        
        q = self.getQueue(name)
        if q is None: return False
        
        if messageClass is not None:
            q.set_message_class(messageClass)
        else:
            messageClass = Message
        
        m = messageClass()
        m.set_body(message)
        q.write(m)
        return True
    
    def readFromQueue(self,name,num=1,visibilityTimeout=None,delete=False):
        '''Read a message from a queue.
        
            Inputs:
                name = name of queue to read from
                num = number of messages to read from queue
                visibilityTimeout = setting this will change the time until the
                    next reader can read the messages received
                delete = true will delete all messages read from the queue
                    
            Returns:
                ResultSet object of messages read. Calling get_body() on one of
                    these messages will return the message it contains. Returns
                    None if queue was not successfully read.
        '''
        if not self.__checkConn(): return None
        
        q = self.getQueue(name)
        if q is None: return None
        
        if visibilityTimeout:
            results = q.get_messages(num_messages=num,
                                     visibility_timeout=visibilityTimeout)
        else:
            results = q.get_messages(num_messages=num)
            
        if delete:
            for m in results:
                q.delete_message(m)
            
        return results
    
    def readFromQueueToFile(self,name,fileName,separator="\n----------\n"):
        '''Dump all the messages from a queue into a local file.
        
            Inputs:
                name = name of queue
                fileName = name of file to dump to
                separator = what to place between messages in the file
            
            Returns:
                True if queue was successfully dumped.
        '''
        if not self.__checkConn(): return False
        
        q = self.getQueue(name)
        if q is None: return False
        
        #why does this boto function have an underscore???
        q.dump_(fileName,sep=separator)
        return True
    
    def deleteQueue(self,name,clear=False):
        '''Delete a queue.
        
            name = name of queue
            clear = if True, will clear the queue before deleting it. This method
                will not delete the queue if it is not empty.
                
            Returns:
                True if queue was successfully deleted. A queue will not be deleted
                    if it still contains messages.
        '''
        if not self.__checkConn(): return False
        
        q = self.getQueue(name)
        if q is None: return False
        
        if clear:
            q.clear()
            
        return self.__conn.delete_queue(q)
        
    def __checkConn(self):
        '''Helper function to make sure SQS connection is open.'''
        if not self.__conn:
            print("[ERROR] must call open() before using this function.")
            return False
        return True
    
if __name__ == "__main__":
    pass
