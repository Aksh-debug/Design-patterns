# LOGGING FRAMEWORK

# The logging framework should support different log levels, such as DEBUG, INFO, WARNING, ERROR, and FATAL.
# It should allow logging messages with a timestamp, log level, and message content.
# The framework should support multiple output destinations, such as console, file, and database.
# It should provide a configuration mechanism to set the log level and output destination.
# The logging framework should be thread-safe to handle concurrent logging from multiple threads.
# It should be extensible to accommodate new log levels and output destinations in the future.


# Entities: Log-levels, LogOutput,  LogMessage
# Patterns: Multiple output destinations - Strategy Pattern, Configuration mechanism - Factory Pattern


from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
import threading


class LogLevel(Enum):
    DEBUG=10
    INFO=20
    WARNING=30
    ERROR=40
    FATAL=50

class LogMessage:
    def __init__(self,log_level:LogLevel,message_content:str):
        self.timestamp=datetime.now()
        self.log_level=log_level
        self.message_content=message_content
    def format(self)->str:
        return f"[{self.timestamp.isoformat()}] [{self.log_level.name}] {self.message_content}"

class LogOutputDestination(ABC):
    @abstractmethod
    def write(self,formatted_message:str):
        pass

class FileOutput(LogOutputDestination):
    def __init__(self,filepath:str):
        self.filepath=filepath
    def write(self,formatted_message:str):
        with open(self.filepath,'a') as f:
            f.write(formatted_message+'\n')
    
class ConsoleOutput(LogOutputDestination):
    def write(self,formatted_message:str):
        print(formatted_message)
        

class DatabaseOutput(LogOutputDestination):
    def __init__(self,connection=None):
        self.connection=connection
    def write(self, formatted_message:str)->None:
        print(f"[DB-WRITE] {formatted_message}")

class LogOutputFactory:
    _outputs={
        "console":ConsoleOutput,
        "file":FileOutput,
        "database":DatabaseOutput
    }
    @classmethod
    def create(cls,output_type:str,**kwargs):
        print(kwargs)
        if(output_type not in cls._outputs):
            raise ValueError(f"Unknown output type: {output_type}")
        return cls._outputs[output_type](**kwargs)

    @classmethod
    def register(cls,name:str,output_cls):
        cls._outputs[name]=output_cls
        


class LoggingManager:
    _instance=None
    _instance_lock=threading.RLock()
    def __new__(cls):
        if(cls._instance is None):
            with cls._instance_lock:
                if(cls._instance is None):
                    cls._instance=super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.level=LogLevel.INFO
        self.outputs=[]
        self._lock=threading.RLock()
    
    def set_log_level(self,level:LogLevel):
        with self._lock:
            self.level=level
    
    def add_output_destination(self,destination:LogOutputDestination):
        with self._lock:
            self.outputs.append(destination) 
    def log(self,level:LogLevel,message_content:str):
        if(level.value<self.level.value):
            return 
        msg=LogMessage(level,message_content)
        formattedMessage=msg.format()
        with self._lock:
            outputs=list(self.outputs)
        for output in outputs:
            output.write(formattedMessage)
    
    def debug(self,message:str):
        self.log(LogLevel.DEBUG,message)    
    def info(self,message:str):
        self.log(LogLevel.INFO,message)    
    def error(self,message:str):
        self.log(LogLevel.ERROR,message)    
    def warning(self,message:str):
        self.log(LogLevel.WARNING,message)    
    def fatal(self,message:str):
        self.log(LogLevel.FATAL,message)    
    

if __name__=='__main__':
    logger = LoggingManager()
    logger.set_log_level(LogLevel.DEBUG)
    logger.add_output_destination(LogOutputFactory.create("console"))
    logger.add_output_destination(LogOutputFactory.create("file", filepath="app.log"))

    logger.debug("Debugging connection pool")
    logger.error("Payment failed for order #123")

    # Anywhere else in the app, LoggingManager() returns the SAME instance
    same_logger = LoggingManager()
    assert logger is same_logger
