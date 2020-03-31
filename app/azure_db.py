#AzureDB Class
#Init a class, Add local variables to the class of
#vars = srv name, db name, pw, 
#Calls getConnection()
import os
from dotenv import load_dotenv

class azure_db:
    def __init__(self):
        #BASEDIR = os.path.abspath(os.path.dirname(__file__))
        #load_dotenv(os.path.join(BASEDIR, '.env'))




        USER_NAME = os.getenv('USER_NAME')
        AZPASSWORD = os.getenv('AZPASSWORD')
        PORT = os.getenv('DBPORT')
        AZURE_SERVER = os.getenv('AZURE_SERVER')
        AZURE_SERVER_SHORT = os.getenv('AZURE_SERVER_SHORT')
        DATABASE = os.getenv('DATABASE')
        
        
        #USER_NAME = os.getenv('USER_NAME')
        #PASSWORD = os.getenv('PASSWORD')
        #PORT = os.getenv('DBPORT')
        #AZURE_SERVER = os.getenv('AZURE_SERVER')
        #AZURE_SERVER_SHORT = os.getenv('AZURE_SERVER_SHORT')
        #DATABASE = os.getenv('DATABASE')

        #print(USER_NAME,PASSWORD,PORT,AZURE_SERVER,AZURE_SERVER_SHORT,DATABASE)

        self.Driver = "{ODBC Driver 17 for SQL Server}"
        self.port = PORT
        self.Timeout = "30"
        self.AzureServer = AZURE_SERVER
        self.AzureServerShort = AZURE_SERVER_SHORT
        self.Db = DATABASE
        self.Username = USER_NAME
        self.Pw = AZPASSWORD


    def getConString(self,):
        return str('DRIVER='+self.Driver+
                   ';Server=tcp:'+self.AzureServer+
                   ','+self.port+';Database='+self.Db+
                   ';Uid='+self.Username+'@'+self.AzureServerShort+
                   ';Pwd='+self.Pw+
                   ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout='+self.Timeout+';"')
