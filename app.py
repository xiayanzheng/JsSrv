#!/usr/bin/python3
#encoding:utf-8
#引用包flask包、安装命令：pip install Flask
import json,sys,os,codecs,time,timedelta
from flask import Flask,jsonify,request,render_template
sys.path.append(r"..")
import AGEOSE as getgeocode
app = Flask(__name__,static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

def genjson(address):
    print(address)
    addresss = address.split('|')
    jsonjar = []
    for x in addresss:
        addressinner = x.split(',')
        getgeocode.Router.SplitInsideAndOutsideSource(object,FOSD=addressinner[1],FromOutsideSource=True)
        # print(getgeocode.Main.Sta)
        geo = getgeocode.Router.SplitInsideAndOutsideResult(object)
        jsonjar.append({"lng":geo[0],"lat":geo[1],"label":addressinner[0],"labelWidth":"48","backgroundColor":"#00B0F0","fontSize":"12","fontColor":""})
    # print(jsonjar)
    currentdir = os.getcwd()
    dyfilename = time.time()
    # file = ('%sData.json'%dyfilename)
    file = ('Data.json')
    file_name = ('%s/static/%s'% (currentdir,file))  # 通过扩展名指定文件存储的数据为json格式
    with codecs.open ( file_name, 'w' , 'utf-8' ) as file_object:
        json.dump(jsonjar, file_object)
    return file

@app.route('/amap',methods=['GET','POST'])
def amap():
    #判断请求方式为POST否则为GET
    if request.method == 'POST':
        address=request.form.get('address', 'default value')#参数不存在时默认default value
        jsondata = genjson(address)
    else:
        address = request.args.get('address', 'default value')#参数不存在时默认default value
        jsondata = genjson(address)
    return render_template("AMapTem.html",JsonData=jsondata)

    # return jsonify({'Success': "1"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)