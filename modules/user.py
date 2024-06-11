import datetime
import random 
import string
from csv  import writer

class users_sessions():
 
    user_session_set = set()
    
    user_set = set()

    def id_generator(num:int=15):
        res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        while res in users_sessions.user_session_set:
            res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
        return res

    class user():
        def __init__(self,username,ipaddress):
            self.username = username
            self.ipaddress = ipaddress
            self.session = users_sessions.id_generator(13)
            users_sessions.user_session_set.add(self.session)
            self.time_of_session = datetime.datetime.now()
            users_sessions.user_set.add(self)
            if self.entry_to_database("login") is False:
                del self
            
        def entry_to_database(self,type:str):
            with open("logs/user_login.csv","a") as file:
                csv_writer = writer(file)
                if type=="login":
                    csv_writer.writerow([self.username,self.ipaddress,self.time_of_session,self.session,type])
                elif type=="logout":
                    csv_writer.writerow([self.username,self.ipaddress,self.time_of_session,self.session,type,datetime.datetime.now()])
                file.close()
                return True
            return False
        
        def delete_user_session(self):
            users_sessions.user_session_set.remove(self.session)
            users_sessions.user_set.remove(self)
            self.entry_to_database("logout")
            del self
            


        
