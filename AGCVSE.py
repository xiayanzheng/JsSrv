import os,time,xlrd,sys
# 为了将多个地址合并在一起需要导入Reduce包
from functools import reduce
# 导入本地库
sys.path.append(r"..")
import Lib.LF as Com

# 创建Main类
class Main():
    time.sleep(1)
    # 定义当前路径
    if getattr(sys, 'frozen', False):
        CurrentPath = os.path.dirname(sys.executable)
    elif __file__:
        CurrentPath = os.path.dirname(__file__)
    else:
        CurrentPath = os.getcwd()
    # 定义SQLite文件的文件名称与路径
    SQLiteDataBaseFile = "AGCV.db"
    SQLiteDataBase = os.path.join(CurrentPath, SQLiteDataBaseFile)
    # 定义输出结果路径的路径为此脚本同目录里的Result文件夹
    ConfigFile = CurrentPath + "\Config\AGCV.ini"
    # 定义输出结果文件的文件名
    ResultFilePath = CurrentPath + "/Results/"
    ResultFileName = ("[%s]%s.csv" % (Com.FormatCurrentTime.YYYYMMDDHHMMSS, Com.Infra.Readini(ConfigFile=ConfigFile, Section="Result", Key="ResultFileName")))
    # 定义输出到结果文件中的标题
    Headers = Com.Infra.Readini(ConfigFile=ConfigFile, Section="Result", Key="Headers").split(",")
    # 实例化以上元素
    def __init__(self, CurrentPath, DataBase, SQLiteDataBase,ResultFilePath,
                 ResultFileName,FullDataWatingList,Headers,ConfigFile,RKM):
        self.CurrentPath = CurrentPath
        self.DataBasePath = DataBase
        self.SQLiteDataBase = SQLiteDataBase
        self.ResultFilePath = ResultFilePath
        self.ResultFileName = ResultFileName
        self.FullDataWatingList = FullDataWatingList
        self.Headers = Headers
        self.ConfigFile = ConfigFile
        self.RKM = RKM

    def Flow(self,UserInputFileRaw):
        global FindedRows,SheetOne,SheetHeaders
        # 定义每次发送请求是可包含的地址最大数量
        # 根据高德的API说明每次只能处理10条以内的数据
        MRPD = 40
        # 让用户将文件拖入
        try:
            UserInputFile = UserInputFileRaw
            # UserInputFile = "E:\\Resources\\Address.xls"
            # 打开Excel文件
            Workbook = xlrd.open_workbook(r"%s" % UserInputFile)
            # 根据Sheet名称获取Sheet内容
            SheetOne = Workbook.sheet_by_name('地址')
            # 获取Excel中的数据行数
            FindedRows = SheetOne.nrows - 1
            # 获取Excel中的标题
            SheetHeaders = SheetOne.row_values(0)
        except:
            print("无法打开此文件,请确认路径里是否有空格")
            sys.exit()
        # 让用户输入数据处理的开始行数
        RowNumberS = int(input("共找到%d条数据,请输入需要处理的数据的开始Excel行数(不能小于1):" % (FindedRows)))
        # 检查用户数的开始行数和结束行数
        if RowNumberS < 1:
            Main.Retry(self, "输入的数值小于1,请重试.")
        else:
            AvailableRows = FindedRows - RowNumberS
            RowNumberE = int(input("共找到%d条数据,请输入需要处理的数据条目数量(不能大于%s条):" % (FindedRows, AvailableRows)))+1
            if RowNumberE > AvailableRows:
                Main.Retry(self, "输入的数值大于%d,请重试." % (int(AvailableRows)))
            elif RowNumberE < 1:
                Main.Retry(self, "输入的数值小于1,请重试.")
            else:
                # 使用本地库Common中的NumberRange方法以最大地址数量创建多个开始行数和结束行数配置
                # 如用户输入开始行数为1结束行数为30 此方法会返回[[1,11],[11, 21],[21, 31],[31, 31]]
                # 这里的行数配置是Excel文件的Excel行数并非由用户定义的行数
                for Range in Com.Numbers.GenRange(self, RowNumberS, RowNumberE, MRPD):
                    # print(Range)
                    # 由于Common中的NumberRange会生成[31,31]这样的范围会导致合并地址报错超出范围
                    # 所以就用Range[0]是否等于Range[1]进行检查如果Range[0]=Range[1]则跳出循环否则使用此配置继续
                    if Range[0] == Range[1]:break
                    else:pass
                    # 获取Range范围内的每一行的数据
                    for Row in range(Range[0], Range[1]):
                        # print(Range[0], Range[1])
                        if len(ConvertAMapGeoCode.AddrListUserInput) < (Range[1] - Range[0]):
                            EachRowOfData = SheetOne.row_values(Row)
                            UserInput = dict(zip(SheetHeaders, EachRowOfData))
                            ConvertAMapGeoCode.AddrListUserInput.append(UserInput)
                        else:pass
                    for UserInputAddr in ConvertAMapGeoCode.AddrListUserInput:
                        ConvertAMapGeoCode.AddrShowCodes.append(str(UserInputAddr["代码"]))
                        ConvertAMapGeoCode.AddrWatingList.append([str(UserInputAddr["经度"]), ',', str(UserInputAddr["纬度"])])
                    Router.SplitInsideAndOutsideSource(self,False,None)
                    ConvertAMapGeoCode.AddrListUserInput.clear()
            Router.SplitInsideAndOutsideResult(self)
        Com.Infra.OpenDir(self,Main.ResultFilePath)
        os.system('pause')
        sys.exit()

    def Retry(self,ErrMsg):
        os.system('cls')
        print(ErrMsg)
        Select = input("[??]是否选择文件并继续?(Y/N)")
        if Select in ["y","Y"]:
            os.system('%s\%s' % (Main.CurrentPath, "AGCV.exe"))
            os.system('cls')
        else:
            os.system('pause')
            sys.exit()



class Router():

    FromOutsideSource = False

    def __init__(self,FromOutsideSource):
        self.FromOutsideSource = FromOutsideSource

    def SplitInsideAndOutsideSource(self, FromOutsideSource, FOSD):
        if FromOutsideSource == False:
            ConvertAMapGeoCode.FromAMapAPI(self, ConvertAMapGeoCode.AddrWatingList)
        else:
            Router.FromOutsideSource = True
            ConvertAMapGeoCode.AddrGeoResult.clear()
            LocalCache = ConvertAMapGeoCode.FromLocalCache(self, Mode='Fetch', Addresses=[FOSD], LocationX=None, LocationY=None)
            # print(LocalCache)
            FOSD = FOSD.split(',')
            if LocalCache == False:
                ConvertAMapGeoCode.FromAMapAPI(self, FOSD)
                print("[**]转换为高德系坐标成功")
            else:
                ConvertAMapGeoCode.AddrGeoResult.append(FOSD)
                Router.SplitInsideAndOutsideResult(self)

    def SplitInsideAndOutsideResult(self):
        if Router.FromOutsideSource == False:
            Com.SaveData.toCSV(self, Main.ResultFilePath, Main.ResultFileName, Main.Headers, ConvertAMapGeoCode.AddrGeoResult)
        else:
            return ConvertAMapGeoCode.AddrGeoResult

class ConvertAMapGeoCode():
    AddrShowCodes = []
    AddrListUserInput = []
    AddrWatingList = []
    AddrGeoResult = []

    def __init__(self,AddrListFromExcel,AddrWatingList,AddrGeoResult,AddrShowCodes):
        self.AddrListUserInput = AddrListFromExcel
        self.AddrWatingList = AddrWatingList
        self.AddrGeoResult = AddrGeoResult
        self.AddrShowCodes = AddrShowCodes

    def FromAMapAPI(self, Locations):
        DataSource = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="AMap", Key="DataSource")
        AccessKey = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="AMap", Key="AccessKey")
        # Coordsys = Common.Infra.Readini(ConfigFile=Main.ConfigFile,Section="AMap",Key="Coordsys")
        if len(Locations) > 4:
            UnionLocations = reduce(lambda x, y: x + y, Com.DaPr.UnpackageListAndInsertValuesAtList(self, Locations, "|"))
        else:UnionLocations = "%s,%s"%(Locations[0],Locations[1])
        ParameterDict = {"key": AccessKey, "locations": UnionLocations,"coordsys":"baidu"}
        # print(ParameterDict)
        try:
            Response = Com.Infra.GetWR(self, DataSource, ParameterDict)
            RawData = Response.json()
            if Router.FromOutsideSource == True:
                LocationXY = str(RawData['locations']).split(",")
                Longitude,Latitude = LocationXY[0],LocationXY[1]
                ConvertAMapGeoCode.AddrGeoResult.append(Longitude)
                ConvertAMapGeoCode.AddrGeoResult.append(Latitude)
                LocationXY = "%s,%s" % (Longitude, Latitude)
                ConvertAMapGeoCode.FromLocalCache(self, Mode='Store', Addresses=LocationXY, LocationX=Longitude,
                                                  LocationY=Latitude)
                # print(Longitude,Latitude)
            else:pass
            for EachRowOfRawData,OrigiAddr,UserInput in zip(RawData["locations"].split("|"),
                                                            ConvertAMapGeoCode.AddrWatingList,
                                                            ConvertAMapGeoCode.AddrListUserInput):
                Result = {}
                AMapLocationXY = EachRowOfRawData.split(',')
                Result['BMapLongitude'] = OrigiAddr[0]
                Result['BMapLatitude'] = OrigiAddr[2]
                Result['AMapLongitude'] = AMapLocationXY[0]
                Result['AMapLatitude'] = AMapLocationXY[1]
                Result = Com.DaPr.MergeTwoDicts(self, Result, UserInput)
                ConvertAMapGeoCode.ReplaceRawDataKey(self, Result)
            for Addr in ConvertAMapGeoCode.AddrShowCodes:
                print("[**]转换为高德系坐标成功%s" % Addr)
        except:
            for Addr in ConvertAMapGeoCode.AddrWatingList:
                print("[!!]转换为高德系坐标失败%s" % Addr)
        ConvertAMapGeoCode.AddrWatingList.clear()
        ConvertAMapGeoCode.AddrListUserInput.clear()

        # time.sleep(1)

    def FromLocalCache(self,Mode,Addresses,LocationX,LocationY):

        if Mode == 'Fetch':
            for Address in Addresses:
                LocalCache = Com.Infra.SQLite3(SQL="select Longitude,Latitude from GeoDataLocalCache WHERE Address = '%s'" % Address,
                                               Data=None, Database=Main.SQLiteDataBase, NumberOfRow=0, OutPutType='List')
                if LocalCache == [] or False:
                    return False
                else:
                    print("[**]在AGCV本地缓存找到相关信息")
                    ConvertAMapGeoCode.AddrGeoResult.append(LocalCache[0])
                    ConvertAMapGeoCode.AddrGeoResult.append(LocalCache[1])
                    return True

        elif Mode == 'Store':
            LocalCacheData = (Addresses, float(LocationX), float(LocationY))
            if Com.Infra.SQLite3(SQL='INSERT INTO GeoDataLocalCache(Address,Longitude,Latitude) VALUES (?,?,?)',
                                 Data=LocalCacheData, Database=Main.SQLiteDataBase, NumberOfRow=None,
                                 OutPutType=None) != False:
                print("[**]AGCV本地缓存写入成功")
                return True
            else:
                return False

    def ReplaceRawDataKey(self, RawData):
        Province = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="Province").split(",")
        City = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="City").split(",")
        District = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="District").split(",")
        Origiaddr = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="Origiaddr").split(",")
        Longitude = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="Longitude").split(",")
        Latitude = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="Latitude").split(",")
        OrigiLongitude = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="OrigiLongitude").split(",")
        OrigiLatitude = Com.Infra.Readini(ConfigFile=Main.ConfigFile, Section="ValueName", Key="OrigiLatitude").split(",")
        RKM = {Province[0]: Province[1], City[0]: City[1], District[0]: District[1], Origiaddr[0]: Origiaddr[1],
               Longitude[0]: Longitude[1], Latitude[0]: Latitude[1], OrigiLongitude[0]: OrigiLongitude[1],
               OrigiLatitude[0]: OrigiLatitude[1]}
        RawData = Com.DaPr.RenameDictKeys(self, RawData, RKM)
        ConvertAMapGeoCode.AddrGeoResult.append(Com.DaPr.FindValidDataInDict(self, Main.Headers, RawData))

if __name__ == '__main__':
    Main.Flow(object)
