class dataplot(object):
    def __init__(self,datatype):
        self.type=datatype
    def print0(self):
        print(self.type) 

    
class tempHumi_dataplot(dataplot):
    def __init__(self,arg1):
        self.arg1=arg1
    def print1(self):
        self.print0
    
if __name__ == "__main__":
    dp1=tempHumi_dataplot('1')
    dp1.print0()
    dp1.print1()