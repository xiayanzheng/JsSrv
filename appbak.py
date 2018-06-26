#!/usr/bin/python3
#encoding:utf-8
#引用包flask包、安装命令：pip install Flask
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)
@app.route('/amapjson',methods=['GET','POST'])
def user():
    #判断请求方式为POST否则为GET
    if request.method == 'POST':
        name=request.form.get('name', 'default value')#参数不存在时默认default value
        print('name:%s' % (name))
    else:
        name = request.args.get('name', 'default value')#参数不存在时默认default value
        print('name:%s' % (name))
    htmlfileP1 = '''
    <!DOCTYPE html><!-- saved from url=(0013)about:internet -->
    <!--3632-->

    <html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no" /><meta http-equiv="Content-Type" content="text/html, charset=utf-8" />
    <title>Maps</title><style type="text/css">html {height: 100%} body {height: 100%;margin: 0px;padding: 0px}
    #main {height: 100%} #panel {position: fixed;background-color: white;max-height: 80%;overflow-y: auto;top: 100px;right: 10px;width: 280px;}.amap-msg{padding: 2px 0;color: #555;background-color: #ff6761;font-size: 12px;white-space: nowrap;position: absolute;border-radius: 5px 5px 5px 0;border: 1px solid #8e8e8e;}
    .amap-msg:after, .amap-msg:before {content: '';display: block;position: absolute;width: 0;height: 0;border: solid rgba(0,0,0,0);border-width: 6px;left: 13px;}
    .adress-name {padding:0 5px;}.amap-msg:after {bottom: -12px;border-top-color: #79ffe7;}  .amap-msg:before {bottom: -13px;border-top-color: #8e8e8e;}  .amap-logo {display: none;}  .amap-copyright {bottom:-100px;display: none;}</style></head>
    <body onLoad="aMap()"><div id="main"></div><div id="panel"></div></body></html>
    <script type="text/javascript" src="http://webapi.amap.com/maps?v=1.4.6&key=8f9f4a282600ea40920d7a72d898da40&plugin=AMap.TruckDriving,AMap.Geocoder,AMap.Transfer,AMap.Driving,AMap.Walking,AMap.Riding,AMap.PlaceSearch,AMap.ToolBar,AMap.MapType,AMap.Weather"></script>
    <script src="http://webapi.amap.com/loca?key=8f9f4a282600ea40920d7a72d898da40"></script>
    <link rel="stylesheet" href="http://cache.amap.com/lbs/static/main.css?v=1.0"/>
    <script type="text/javascript" src="http://cache.amap.com/lbs/static/PlaceSearchRender.js"></script>
    <script type="text/javascript" src="http://a.amap.com/Loca/static/dist/jquery.min.js"></script>
    <script type="text/javascript" src="http://webapi.amap.com/ui/1.0/main.js"></script>
    <script src="http://libs.baidu.com/jquery/2.1.1/jquery.min.js"></script>
    <script type="text/javascript" src="Address.xls.json"></script>
    <script type="text/javascript">
    var map;
    var toolbar;
    var maptype;
    function aMap()
        {
        map = new AMap.Map('main',{resizeEnable: true,zoom:8,center: [110.465659, 23.038419]});
        map.addControl(toolbar=new AMap.ToolBar());
        map.addControl(maptype=new AMap.MapType());
        addMapStyle();'''
    htmlfileP2 = ''' // var datas = [{lng:110.118193,lat:22.69139,label:['西岸小学'],labelWidth:48,backgroundColor:'#00B0F0',fontSize:12,fontColor:''},{lng:110.156788,lat:22.696242,label:['高山小学'],labelWidth:48,backgroundColor:'#00B0F0',fontSize:12,fontColor:''},{lng:110.151924,lat:22.689291,label:['玉州区城北二中'],labelWidth:84,backgroundColor:'#FFFFFF',fontSize:12,fontColor:''},{lng:110.156411,lat:22.687206,label:['城北初中'],labelWidth:48,backgroundColor:'#FFFFFF',fontSize:12,fontColor:''},{lng:110.15575,lat:22.68372,label:['潘岭小学'],labelWidth:48,backgroundColor:'#00B0F0',fontSize:12,fontColor:''},{lng:110.204446,lat:22.684368,label:['师范学院东校区'],labelWidth:84,backgroundColor:'#FFFFFF',fontSize:12,fontColor:''},{lng:110.207777,lat:22.684796,label:['好孩子幼儿园'],labelWidth:72,backgroundColor:'#FFC000',fontSize:12,fontColor:''}];'''
    htmlfileP3 = '''	//var datas = JSON.parse("Address.xls.json");
    $.getJSON("Address.xls.json", function(json) {
    addLableMarker(json); // this will show the info it in firebug console
});

    // addLableMarker(datas);

function addLableMarker(datas) {
var driOptions = {map : map,content:" ",policy:0,size:1,city:'beijing'};
var driving = new AMap.TruckDriving(driOptions);
var path = [];
    for (var i = 0; i < datas.length; i++) {
		var pointData = datas[i];
        var mapOptions = {
				map : map,
				position : [ pointData.lng, pointData.lat],
				content:" "
			};
        var marker = new AMap.Marker(mapOptions);
        path.push({lnglat:mapOptions.position});//起点
        if (pointData.image) {
            mapOptions.icon = pointData.image;
        }
        //
        if (!pointData.labelWidth) {
            pointData.labelWidth=80;
        }
        // 设置label标签
        var label = "<div style='position: absolute;right: 10px;padding: 10px;width:"+pointData.labelWidth+"px;word-break: break-all;white-space:normal;background-color:"+pointData.backgroundColor+"'>";
        if (pointData.label) {
            for (var j = 0; j < pointData.label.length; j++) {
                label += "<span style='text-align:right;list-style-type:none;font-size:"+pointData.fontSize+"px;color:"+pointData.fontColor+";'>"
                        + pointData.label[j] + "</span>"
            }
            label += "</div>";
        }
        marker.setLabel({//label默认蓝框白底左上角显示，样式className为：amap-marker-label
            zIndex: 200,
            offset : new AMap.Pixel(0, 0),//修改label相对于maker的位置左右/上下
            content : label});
		}
driving.search(path,function(status, result){});
	}
map.setMapStyle();
}

function addMapStyle()
{
 var domHtml = "<div style='position: absolute;bottom:20px;right:5px;height: 21px;' >"
        +"<select style='border: 1px #dbd9d9 solid;width: 80px;margin: 10px;height: 25px;' id='mapStyle'>"
        +"<option style ='border: 1px #ccc solid;' value ='normal'>标准</option>"
        +"<option style ='border: 1px #ccc solid;' value ='whitesmoke'>远山黛</option>"
        +"<option style ='border: 1px #ccc solid;' value='macaron'>马卡龙</option>"
        +"<option style ='border: 1px #ccc solid;' value='graffiti'>涂鸦</option>"
        +"<option style ='border: 1px #ccc solid;' value='darkblue'>极夜蓝</option>"
        +"<option style ='border: 1px #ccc solid;' value='blue'>靛青蓝</option>"
        +"<option style ='border: 1px #ccc solid;' value='fresh'>草色青</option>"
        +"<option style ='border: 1px #ccc solid;' value='dark'>幻影黑</option>"
        +"<option style ='border: 1px #ccc solid;' value='light'>月光银</option>"
        +"<option style ='border: 1px #ccc solid;' value='grey'>雅士灰</option>"
        +"</select></div>"
 $('#main').append(domHtml);
 $('#mapStyle').change(function(){
        map.setMapStyle('amap://styles/'+$(this).val());
    });

 };</script>
    '''
    htmlfile = htmlfileP1+htmlfileP2+htmlfileP3
    return htmlfile

    # return jsonify({'Success': "1"})
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("8999"))