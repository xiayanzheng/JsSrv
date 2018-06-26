#!/usr/bin/python3
#encoding:utf-8
#引用包flask包、安装命令：pip install Flask
import json,sys,os,codecs
from flask import Flask,jsonify,request,render_template
sys.path.append(r"..")
import AGEOSE as getgeocode
import ACTA as getaddrbycode
from Lib.LF import DaPr
app = Flask(__name__,static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


def addrrouter(addrtype,address):
    if addrtype == 'addrg':
        return getgeobyaddr(address)
    else:
        return getgeobycode(addrtype,address)

def getgeobyaddr(address):
    addressinner = address.split(',')
    getgeocode.Router.SplitInsideAndOutsideSource(object, FOSD=addressinner[1], FromOutsideSource=True)
    geo = getgeocode.Router.SplitInsideAndOutsideResult(object)
    return {"lng":geo[0],"lat":geo[1],"label":addressinner[0]}

def getgeobycode(addrtype,address):
    addressinner = getaddrbycode.GetAddr.By(object,Mode=addrtype,Code=address)
    getgeocode.Router.SplitInsideAndOutsideSource(object, FOSD=addressinner, FromOutsideSource=True)
    geo = getgeocode.Router.SplitInsideAndOutsideResult(object)
    return {"lng":geo[0],"lat":geo[1],"label":address}


def genjson(addresses,addrtype):
    # print(address)
    addresses = addresses.split('|')
    jsonjar = []
    for address in addresses:
        # AGEO Debug Tunnel
        # print(getgeocode.Main.Sta)
        geo = addrrouter(addrtype,address)
        lable = {"labelWidth":"48","backgroundColor":"#00B0F0","fontSize":"12","fontColor":""}
        jsonjar.append(DaPr.MergeTwoDicts(object,geo,lable))
    # print(jsonjar)
    currentdir = os.getcwd()
    file = ('Data.json')
    file_name = ('%s/static/%s'% (currentdir,file))
    with codecs.open ( file_name, 'w' , 'utf-8' ) as file_object:
        json.dump(jsonjar, file_object)
    return file

@app.route('/amap',methods=['GET','POST'])
def amap():
    if request.method == 'POST':
        address=request.args.get('address', 'default value')
        addrtype = request.args.get('addrtype', 'default value')
        jsondata = genjson(address,addrtype)
    else:
        address = request.args.get('address', 'default value')
        addrtype = request.args.get('addrtype', 'default value')
        jsondata = genjson(address,addrtype)
    return render_template("AMapTem.html",JsonData=jsondata)

    # return jsonify({'Success': "1"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)