# To actually have your app use this file, you need to RENAME the file to db_credentials.py
# You will find details about your CS340 database credentials on Canvas.

# the following will be used by the webapp.py to interact with the database
# You can also use environment variables

# For Local Devlelopment
#host = 'localhost'
#user = 'root'                                   # can be different if you set up another username in your MySQL installation
#passwd = 'nottellingyou'                        # set accordingly
#db = 'bsg'


# For OSU Flip Servers
load_dotenv(dotenv_path)

host = os.environ.get("340DBHOST")    # MUST BE THIS
user = os.environ.get("340DBUSER")       # don't forget the CS_340 prefix
passwd = os.environ.get("340DBPW")               # should only be 4 digits if default
db = os.environ.get("340DB")