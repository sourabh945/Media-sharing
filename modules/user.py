import datetime
import random 
import string
from csv  import writer

class users_sessions():
 
    user_id = set()

    def id_generator(num:int=15):
        res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        while res in users_sessions.user_id:
            res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        return res

    class user():
        def __init__(self,username,ipaddress):
            self.username = username
            self.ipaddress = ipaddress
            self.session = users_sessions.id_generator(13)
            users_sessions.user_id.add(self.session)
            self.time_of_session = datetime.datetime.now()
            if self.entry_to_database() is False:
                del self
            
        def entry_to_database(self):
            with open("logs/user_login.csv","a") as file:
                csv_writer = writer(file)
                csv_writer.writerow([self.username,self.ipaddress,self.time_of_session,self.session])
                file.close()
                return True
            return False


        
