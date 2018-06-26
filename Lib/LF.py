import requests,os,time,csv,sqlite3,subprocess,configparser,pymysql,xlrd,codecs
import urllib.parse as parse
from xlutils.copy import copy
from functools import reduce
from xlwt import Style

class ErrMsg():

    UnsupportStr = "不支持输入字符"
    UnableAccessThisFile = "另一个程序正在使用此文件，进程无法访问。"
    def __init__(self,UnsupportStr,UnableAccessThisFile):
        self.UnsupportStr = UnsupportStr
        self.UnableAccessThisFile = UnableAccessThisFile

class Msg():
    StartGetToken = "开始获取Token"
    GetTokenSuccess = "获取Token成功"
    StartGetData = "开始获取数据"
    GetDataSuccess = "获取数据成功"
    StartWriteData = "开始写入数据"
    WriteDataSuccess = "写入数据成功!"
    NoNetWorkConnection = "没有网络连接,请重试"
    ContinueOrQuit = "按任意键继续或按Q退出"
    UnsupportedDB = "不支持此类型数据库"
    WrongDataFormat = "API返回的数据格式错误,请重试"
    UnknowProfileID = "未知的配置项,请重试."
    SelectProfile = "请选择一项配置进行数据下载与分析"
    SelectProfileUpline = "=[ID]=[Profile]==========="
    SelectProfileDownline = "=========================="
    CopyFileToRawData = "复制文件到RawData文件夹"
    CallMergeBat = "调用Merge.bat"
    CopyFileToData = "复制文件到Data文件夹"
    CallStartBat = "调用Start.bat"
    OpenDataFolder = "打开Data文件夹"
    FailedGetAccentToken = "获取AccentToken失败请重试"
    ContinueOrQuitForRetryFunction = "已尝试10次,是否需要继续重试10次?"
    TimeCountOfRetry = "正在重试第<<%s>>次"
    UnknowSelection = "UnknowSelection"

    def __init__(self, StartGetToken, GetTokenSuccess, StartGetData, StartWriteData,
                 WriteDataSuccess, NoNetWorkConnection, WrongDataFormat, UnknowProfileID,
                 SelectProfile, SelectProfileUpline, SelectProfileDownline, CopyFileToRawData,
                 CallMergeBat, CopyFileToData, CallStartBat, OpenDataFolder, FailedGetAccentToken, UnknowSelection):
        self.StartGetToken = StartGetToken
        self.FinishGetToken = GetTokenSuccess
        self.StartGetData = StartGetData
        self.StartWriteData = StartWriteData
        self.WriteSuccess = WriteDataSuccess
        self.NoNetWorkConnection = NoNetWorkConnection
        self.WrongDataFormat = WrongDataFormat
        self.UnknowProfileID = UnknowProfileID
        self.SelectProfile = SelectProfile
        self.SelectProfileUpline = SelectProfileUpline
        self.SelectProfileDownline = SelectProfileDownline
        self.CopyFileToRawData = CopyFileToRawData
        self.CallMergeBat = CallMergeBat
        self.CopyFileToData = CopyFileToData
        self.CallStartBat = CallStartBat
        self.OpenDataFolder = OpenDataFolder
        self.FailedGetAccentToken = FailedGetAccentToken
        self.UnknowSelection = UnknowSelection

class DataFormat():
    def MergeMultiTupleList(TupleList):
        List = []
        for Tuple in TupleList:
            for Data in Tuple:
                List.append(Data)
        return List

class Infra():

    def OpenDir(self,Dir):
        os.system("explorer %s" % DaPr.ReplaceDirSlash(self,Dir))

    def PostWR(self, DataSource, Parameter):
        Counter = 0
        Response = Infra.Post(self, DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = Infra.Post(self, DataSource, Parameter)
                else:
                    break
            else:
                Response = Infra.Post(self, DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def GetWR(self, DataSource, Parameter):
        Counter = 0
        Response = Infra.Get(self, DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = Infra.Get(self, DataSource, Parameter)
                else:
                    break
            else:
                Response = Infra.Get(self, DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def Post(self, DataSource, Parameter):
        try:
            # 构造并发送Post请求
            Request = requests.post(DataSource, Parameter)
            # 定义返回数据变量名称
            Response = Request.json()
            # 返回响应报文
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def Get(self, DataSource, ParameterDict):
        try:
            # 构造并发送Get请求(在APIUrl后加入查询参数的字典)
            Request = "%s?%s" % (DataSource, parse.urlencode(ParameterDict))
            # Request = RawRequest.encode("utf-8")
            # print(Request)
            # 定义返回报文变量名称
            Response = requests.get(Request)
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            # time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def MariaDB(SQL, Host, Port, User, Password, Database, CharSet, Data, NumberOfRow, ):
        try:
            # 连接MySQL数据库
            ConnectDataBase = pymysql.connect(host=Host, port=Port, user=User, password=Password, db=Database,
                                              charset=CharSet,cursorclass=pymysql.cursors.DictCursor)
            # 通过cursor创建游标
            DataBaseCursor = ConnectDataBase.cursor()
            # 执行数据查询
            DataBaseCursor.execute(SQL)
            if Data == "None":
                DataBaseCursor.execute(SQL)
                if NumberOfRow == 1:
                    RawData = DataBaseCursor.fetchone()
                    ConnectDataBase.close()
                    return RawData
                if NumberOfRow > 0:
                    RawData = DataBaseCursor.fetchmany(NumberOfRow)
                    ConnectDataBase.close()
                    return RawData
                else:
                    RawData = DataBaseCursor.fetchall()
                    ConnectDataBase.close()
                    return RawData
            else:
                DataBaseCursor.execute(SQL)
                ConnectDataBase.commit()
                ConnectDataBase.close()
                return True
        except:
            return False

    def SQLite3(SQL, Data, OutPutType, NumberOfRow, Database):
        try:
            ConnectDataBase = sqlite3.connect(Database)
            CursorDataBase = ConnectDataBase.cursor()

            if Data == None:
                SQLS = CursorDataBase.execute(SQL)
                if NumberOfRow == 1:
                    RawData = SQLS.fetchone()
                elif NumberOfRow > 0:
                    RawData = SQLS.fetchmany(NumberOfRow)
                else:
                    RawData = SQLS.fetchall()
                if OutPutType == "List":
                    return DataFormat.MergeMultiTupleList(RawData)
                else:
                    return RawData
            else:
                CursorDataBase.execute(SQL, Data)
                ConnectDataBase.commit()
        except:
            # print("[!!]数据库写入失败请联系yzxia@hitachi-systems.cn")
            return False

    def SQLite3Debug(SQL, Data, OutPutType, NumberOfRow, Database):
        ConnectDataBase = sqlite3.connect(Database)
        CursorDataBase = ConnectDataBase.cursor()

        if Data == None:
            SQLS = CursorDataBase.execute(SQL)
            if NumberOfRow == 1:
                RawData = SQLS.fetchone()
            elif NumberOfRow > 0:
                RawData = SQLS.fetchmany(NumberOfRow)
            else:
                RawData = SQLS.fetchall()
            if OutPutType == "List":
                return DataFormat.MergeMultiTupleList(RawData)
            else:
                return RawData
        else:
            CursorDataBase.execute(SQL, Data)
            ConnectDataBase.commit()

    def ExcuteBat(self, BatFilePath,BatFile):
        BatFilePath = ("%s\\%s" % (BatFilePath, BatFile))
        ExcuetBat = subprocess.Popen("cmd.exe /c" + "%s abc" % BatFilePath, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Curline = ExcuetBat.stdout.readline()
        while (Curline != b''):
            # print(Curline.decode('GBK'))
            Curline = ExcuetBat.stdout.readline()
        ExcuetBat.wait()
        # print(ExcuteBat.returncode)
        ExcuetBat.terminate()

    def Readini(ConfigFile,Section,Key):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        # ReadConfig.sections()
        ReadConfig.options(Section)
        # ReadConfig.items(Section)
        Value = ReadConfig.get(Section, Key)
        return Value

    def ReadiniAsDict(ConfigFile):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        Dict = dict(ReadConfig._sections)
        for Key in Dict:
            Dict[Key] = dict(Dict[Key])
        return Dict

class SaveData():

    def toCSV(self, FilePath, FileName, Headers, Data):
        LogPath = ("%s%s" % (FilePath, FileName))
        print(Msg.StartWriteData)
        with open(LogPath, 'w',newline='') as CSV:
            # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
            Writer = csv.DictWriter(CSV, fieldnames=Headers)
            # 写入列名称(字典的键)
            Writer.writeheader()
            # 循环写入列表中每一条数据到CSV文件
            for Row in Data:
                # 写入元素(字典的值)
                Writer.writerow(Row)
        print(Msg.WriteDataSuccess)
        CSV.close()

    def toCSVSR(self,CSV,Headers, Data):
        # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
        Writer = csv.DictWriter(CSV, fieldnames=Headers)
        # 写入列名称(字典的键)
        Writer.writeheader()
        # 写入元素(字典的值)
        Writer.writerow(Data)
        # print(Msg.WriteDataSuccess)
        CSV.close()

    def toTXT(self, FilePath, FileName, Data):
        # 定义文件路径
        LogPath = ("%s\%s" % (FilePath, FileName))
        # 打开文件
        with open(LogPath, 'w', encoding='utf-8') as Log:
            # 写入数据
            Log.write(Data)
            # 输出"写入数据成功数据"
            print(Msg.WriteDataSuccess)
            # 打开数据存储文件夹
            os.system("explorer.exe %s\Logs" % FilePath)
        return LogPath

    def toXls(self, File, Row, Col, Str, Style=Style.default_style):
        # 合并单元格:
        # ws.write_merge(top_row, bottom_row, left_column, right_column, string)
        rb = xlrd.open_workbook(File, formatting_info=True)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        ws.write(Row, Col, Str, Style)
        wb.save(File)

    def ModifyExcel(self,FilePath,Filename,RowColSet,Data):
        book = xlrd.open_workbook(Filename)  # 打开excel
        new_book = copy(book)  # 复制excel
        sheet = new_book.get_sheet(0)  # 获取第一个表格的数据
        for RowCol in RowColSet:
            sheet.write(RowCol[0], RowCol[1], Data)  # 修改0行1列的数据为'Haha'
        TempFile = FilePath + '\Temp.xls'
        new_book.save(TempFile)  # 保存新的excel
        try:
            os.remove(Filename)  # 删除旧的excel
            os.rename(TempFile, Filename)  # 将新excel重命名
        except:print(ErrMsg.UnableAccessThisFile)

class FormatCurrentTime():
    YYYYMMDDHHMMSS = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    YYYYMMDD = time.strftime("%Y%m%d", time.localtime())
    def __init__(self,YYYYMMDDHHMMSS,YYYYMMDD):
        self.YYYYMMDDHHMMSS = YYYYMMDDHHMMSS
        self.YYYYMMDD = YYYYMMDD

class Numbers():

    def GenRange(self, StartNumber, EndNumber, GapNumber):
        NumberRangeResult = []
        RowNumberSP = StartNumber
        Gap = int(EndNumber) - int(StartNumber)
        if Gap > GapNumber:
            for X in range(int(Gap / GapNumber)):
                Temp = []
                Temp.append(RowNumberSP)
                Temp.append(RowNumberSP + GapNumber)
                NumberRangeResult.append(Temp)
                RowNumberSP += GapNumber
            Temp = []
            Temp.append(RowNumberSP)
            Temp.append(RowNumberSP + int(Gap % GapNumber))
            NumberRangeResult.append(Temp)
            RowNumberSP += int(Gap % GapNumber)
        else:
            NumberRangeResult.append([StartNumber,EndNumber])
        return NumberRangeResult

    def NumCheck(self, Input, Maximum, Minimum, Max, Plus):

        if Maximum != None:
            while Input > Maximum:
                print("输入的数值大于%d,请重试." % Maximum)
            else:
                return Input + Plus
        elif Minimum != None:
            while Input < Minimum:
                print("输入的数值小于%d,请重试." % Minimum)
            else:
                return Input + Plus
        elif Maximum and Minimum != None:
            while Input > Maximum and Input < Minimum:
                print("输入的数值超出区间")
            else:return Input + Plus

        #
        # if RowNumberE > MaximumRowOfData:
        #     Main.Retry(self, )
        # elif RowNumberE > int(SheetRows):
        #     Main.Retry(self, "输入的数值大于%d,请重试." % (int(SheetRows) - 1))
        # elif RowNumberE < 1:
        #     Main.Retry(self, "输入的数值小于1,请重试.")
        # else:
        #     int(RowNumberE) + 1

class DaPr():

    def ReplaceDirSlash(self,Dir):
        return reduce(lambda x, y: x + y, DaPr.InsertIntoValuesAtList(self,Dir.split("/"),"\\"))

    def RenameDictKeys(self,RawData,ReplaceKeyMap):
        for Key in RawData:
            for RDKey, RDVaule in ReplaceKeyMap.items():
                if Key == RDKey:
                    RawData[RDVaule] = RawData.pop(Key)
        return RawData

    def InsertIntoValuesAtList(self, DataSet, InsertValue):
        UnionData = []
        for Data in DataSet:
            UnionData.append(Data)
            UnionData.append(InsertValue)
        del UnionData[-1]
        return UnionData

    def InsertIntoXValuesAtList(self, DataSet, Gap, InsertValue):
        UnionData = []
        Count = 0
        if len(DataSet) > Gap:
            for Data in DataSet:
                if Count < Gap:
                    UnionData.append(Data)
                    Count += 1
                else:
                    UnionData.append(InsertValue)
                    Count = 0
            del UnionData[-1]
        else:
            for Data in DataSet:
                UnionData.append(Data)
        return UnionData

    def UnpackageListAndInsertValuesAtList(self, DataSet, InsertValue):
        UnionData = []
        for List in DataSet:
            for Data in List:
                UnionData.append(Data)
            UnionData.append(InsertValue)
        del UnionData[-1]
        return UnionData

    def MergeTwoDicts(self,DictA,DicB):
        MergedDict = {}
        for Key, Value in DictA.items():
            MergedDict[Key] = Value
        for Key, Value in DicB.items():
            MergedDict[Key] = Value
        return MergedDict

    def FindValidDataInDict(self, List, Dict):
        ValidData = {}
        for Key, Value in Dict.items():
            if Key in List:
                ValidData[Key] = Value
        return ValidData
