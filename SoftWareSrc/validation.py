import time


V_SUCCESS=1

class validation:
    username = ["","","","","","","","","",""]                       #最多允许八个账户允许
    passward = ["","","","","","","","","",""]
    last_time = [0,0,0,0,0,0,0,0]                                    #时间记录单位，一天一变
    count = [0,0,0,0,0,0,0,0] 
    accountnum = 0
    def __init__(self):
        fo = open("validationname .txt",'r')
        self.accountnum = len(fo.readlines())
        accountnum = self.accountnum
        fo.close()                                                   #统计账号数
        fo = open("validationname .txt",'r')
        for i in range(0,accountnum):
            self.username[i] = fo.readline()
            self.username[i] = self.username[i].strip('\n')
        fo.close()
        fi = open("validationpassward.txt",'r')
        for i in range(0,accountnum):
            self.passward[i] = fi.readline()
            self.passward[i] = self.passward[i].strip('\n')
        fi.close()
        for i in range(0,accountnum):
            self.last_time[i] = time.time()
    def LoginCheck(self, username ,passward):
        if self.dataCheck(username , passward) == -1:
            return -1
        elif self.frequencyCheck(username, passward) == -1:
            return -2
        else:
            return 1
    def dataCheck(self, usernames ,passwards):
        #print("输入值",usernames,passwards)
        for i in range (0 ,self.accountnum):
           # print(self.username[i]," ",usernames)
            if(self.username[i] == usernames):
               # print("pandingweizhi",self.username[i],usernames)
                if(self.passward[i] == passwards):
                   # print(self.passward(),passwards)
                    return 1
                else:
                    return -1
        return -1
    def frequencyCheck(self, usernames ,passwards):
        for i in range (0 ,self.accountnum):
            if(self.username[i] == usernames):
                times = time.time() - self.last_time[i]
                self.last_time[i] = time.time();
                #print("时间差：",times)
                if(times<0.01):                                     #两次最大时间间隔设置为0.01秒
                    self.count[i] = self.count[i] + 1
                    if(self.count[i]>100):
                        self.count[i] = self.count[i] - 1
                        #print("ceshi",self.count[i])
                        return -1
                    elif(self.count[i] <= 100):
                        return 1
                elif(times >= 0.01):
                    if(self.count[i]>0):
                        self.count[i] = self.count[i] - 1
                    return 1
    #def ceshi(self):                        #初始化无问题
    #    for i in range(0,self.accountnum):
    #        print(self.passward[i])
    #    for i in range(0,self.accountnum):
    #        print(self.username[i])
    #    for i in range(0,self.accountnum):
    #        print(self.last_time[i])
    #    for i in range(0,self.accountnum):
    #        print(self.count[i])



if __name__=='__main__':


    classs = validation()
    username = "sfgdfrf@163.com"
    passward = "fgerfrefszf"
    #classs.ceshi()
    #print("之后是执行结果")
    for i in range(1,1000):
        time.sleep(0.001)
        print(classs.LoginCheck(username,passward),"  ",i)
    for i in range(1,50):
        time.sleep(0.1)
        print(classs.LoginCheck(username,passward),"  ",i)
    for i in range(1,1000):
        time.sleep(0.001)
        print(classs.LoginCheck(username,passward),"  ",i)



