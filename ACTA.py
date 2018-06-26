import os,time,xlrd,sys
# 为了将多个地址合并在一起需要导入Reduce包
from functools import reduce
# 导入本地库
sys.path.append(r"..")
import Lib.LF as Com

class GetAddr():
    time.sleep(1)
    # 定义当前路径
    if getattr(sys, 'frozen', False):
        CurrentPath = os.path.dirname(sys.executable)
    elif __file__:
        CurrentPath = os.path.dirname(__file__)
    else:
        CurrentPath = os.getcwd()
    Sta = []
    SQLiteDataBaseFile = "AGEO.db"
    SQLiteDataBase = os.path.join(CurrentPath, SQLiteDataBaseFile)

    def __init__(self,SQLiteDataBase,Sta):
        self.SQLiteDataBase = SQLiteDataBase
        self.Sta = Sta

    def By(self,Mode,Code):

        if Mode == 'code':
            Addr = Com.Infra.SQLite3(SQL="select Addr from JsSrvAGEOMaster WHERE Code = '%s'" % Code,
                                           Data=None, Database=GetAddr.SQLiteDataBase, NumberOfRow=0, OutPutType='List')
            if Addr == []:return False
            else:
                print("[**]通过Code查询地址成功")
                return Addr[0]

        if Mode == 'codename':
            Addr = Com.Infra.SQLite3(
                SQL="select Addr from JsSrvAGEOMaster WHERE CodeName = '%s'" % Code,
                Data=None, Database=GetAddr.SQLiteDataBase, NumberOfRow=0, OutPutType='List')
            if Addr == []:
                return False
            else:
                print("[**]通过CodeName查询地址成功")
                return Addr[0]
