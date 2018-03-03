from django.shortcuts import render

import re
from django.http import HttpResponse
import qrcode
import os
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
import json, urllib
from urllib.parse import urlencode

import datetime 
import time
from django import forms
from django.shortcuts import render_to_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from shopApp.mytool import *
from django.db import connection
from aip import  AipSpeech
import json
import base64
import subprocess
xx="";

def home(request):
    is_login = request.session.get('IS_LOGIN')
    print(is_login)
    
    return render(request , "base.html");


def error(request):
    return HttpResponse("我是404");

def adsecondkill(request):
    return render(request , "adsecondkill.html");
def secondkillManage(request):
    return render(request , "secondkillManage.html");

def goodsManage(request):
    baseSelectName = ''
    try:
        baseSelectName = request.POST["baseSelectName"]
        
        print(baseSelectName)
    except:
        pass
    Dict = {'baseSelectName':baseSelectName}
    print(baseSelectName)
    if baseSelectName == "":
        return render(request , "goodsManage.html");
    else:
        return render(request , "goodsManage.html" , {'Dict':json.dumps(Dict)});
    


def adPage(request):
    return render(request , "adPage.html");
# 生成随机验证码
def identificode(request):
    aaa = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','j','k','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','J','K','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    bg= (0 , 255 ,200)
    backcolor= (random.randint(32, 128), random.randint(32, 128), random.randint(32, 128))
    w = 60 * 4;
    h = 60
    # 创建一张图片，指定图片mode，长宽
    image = Image.new('RGB', (w, h), (255,182,193))
    # 设置字体类型及大小
    font = ImageFont.truetype(font='./shopApp/static/font/handan.ttf', size=36)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 遍历给图片的每个像素点着色
    for x in range(w):
        for y in range(h):
            draw.point((x, y),fill=bg)
    # 将随机生成的chr，draw如image
    global xx;
    xx = "";
    for t in range(4):
        a=aaa[random.randint(0 , 57)];
        # temp = randomChar()
        draw.text((60 * t + 10, 10), a, font=font,fill=backcolor)
        xx=xx+a;
    # 设置图片模糊
    xx=str.lower(xx);#大写字母转小写
    image = image.filter(ImageFilter.BLUR)
    # 保存图片
    image.save('./shopApp/static/myfile/code.jpg', 'jpeg')
    imgDic = {"imgPath":"static/myfile/code.jpg"}
    return HttpResponse(json.dumps(imgDic) , content_type = "application/json")
def userManage(request):
    return render(request , "userManage.html");

def orderManage(request):
    return render(request , "orderManage.html");

def adManage(request):
    return render(request , "adManage.html");

def cartsManage(request):   
    return render(request , "cartsManage.html");

def activeManage(request):

    return render(request , "activeManage.html");

def addGoods(request):
    
    return render(request, "goodsAdd.html")
def changeLunbo(request):
    return render(request,"addLunbo.html")

def recomendGoods(request):
    return render(request,"recomendGoods.html")




#改变轮播图界面
def changePic(request):
    # a = request.POST["goodsid"];
    # print(a);
    return render(request,"changePic.html");

def drawManage(request):
    return render(request,"drawManage.html")

# 登录界面
def login(request):
    request.session['IS_LOGIN'] = True
    return render(request , "login.html");


# 登录接口 (ok)
def loginApi(request):
    global xx; 
    userName = request.POST["username"]
    password = request.POST["password"]
    code=request.POST["code"]
    code=str.lower(code);
    if xx==code:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM manager WHERE username=\"%s\" AND pwd=\"%s\"'%(userName , password))
        a = cursor.fetchall()
        cursor.close()
        if a:
            successMSG = MyTool.resultOk("登陆成功");
            return HttpResponse(json.dumps(successMSG) , content_type="application/json")
        else: 
            errorMSG = MyTool.resultError("登录失败");
            return HttpResponse(json.dumps(errorMSG) , content_type="application/json")
    else:
        errorMSG = MyTool.resultError("验证码错误");
        return HttpResponse(json.dumps(errorMSG) , content_type="application/json")
# 用户添加接口
def userManageJsonAdd(request):
    if request.POST["username"]:
        username = request.POST["username"]
    if request.POST["password"]:
        pwd = request.POST["password"]

    
    userid = randomString()
    data = {"username":username , "password":pwd};
    imgName = randomString()+".jpg"
    img_file = r"./shopApp/static/myfile/" + imgName
    img = qrcode.make(data)
    img.save(img_file)

    cursor = connection.cursor();
    cursor.execute("SELECT * FROM user")
    datas=cursor.fetchall()
    cursor.close()
    print("**************88")
    print()
    for i in datas:
        if i[1] == username:
            
            statusDic=MyTool.resultError("用户已存在")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
            break;
    cursor = connection.cursor();
    result = cursor.execute("INSERT INTO user(userid , username , pwd , qrcode)VALUES('%s' , '%s' , '%s' , '%s')"%(userid , username , pwd , imgName))
    cursor.close()
    statusDic = "";
    print("&&&&&&&&&&&")
    if result == 1:
        
        statusDic = MyTool.resultOk("添加用户成功");
        redpackAddCurrency(userid, "注册", "3")
    else :
        
        statusDic = MyTool.resultError("添加用户失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");


# 用户查询接口
def userManageJsonSelect(request):
    if request.POST and (request.POST['username'] !="" or request.POST['phone'] != ""):
        username = request.POST['username'].replace(" ","");
        phone = request.POST['phone'].replace(" ","");

        # if username =="" and phone == "":
        #     return HttpResponse(json.dumps({'data':allUsertables, 'status':'用户名和手机号为空'}), content_type="application/json");
        if username == "" and phone !="":
            sql = "SELECT * FROM user where phone like '%%%%%s%%%%'" % phone;
        elif phone == "" and username != "":
            sql = "SELECT * FROM user where username like '%%%%%s%%%%'" % username;
        else:
            sql = "SELECT * FROM user where username like '%%%%%s%%%%' or phone like '%%%%%s%%%%'" % (username, phone);
    else:
        sql = "SELECT * FROM user" ;

    cursor=connection.cursor()
    
    allUsertables = []

    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            usertable = {
                'userid':row[0],
                'username':row[1],
                'headimg':row[2],
                'phone':row[3],
                'pwd':row[4],
                'wxid':row[5],
                'acountmoney':row[6],
                'rewardmoney':row[7],
                'activecode':row[8],
                'redpack':row[9],
                'upperson':row[10],
                'downperson':row[11],
                'rebate':row[12],
                'integral':row[13],
                'bankcard':row[14],
                'power':row[15],
                'address':row[16],
                'registetime':str(row[17]),
            }
            allUsertables.append(usertable)
            cursor.close();
        return HttpResponse(json.dumps({'data':allUsertables, 'status':'ok'}), content_type="application/json")
   
    except Exception as e:    
            return HttpResponse(json.dumps({'data':allUsertables, 'status':'error'}), content_type="application/json");

def userManageJsonDelete(request):
    for key in request.POST:
        userid = request.POST.getlist(key)[0]

    #删除头像图片
    cursor=connection.cursor();
    headimg = ""
    cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid));
    datas = cursor.fetchall()
    for data in datas:
        headimg = data[2]  
    # print(headimg)
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == headimg:
            os.remove("../shopServer/shopApp/static/myfile/"+headimg);
    cursor.close();

    #删除二维码图片
    cursor=connection.cursor();
    secondimg = ""
    cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid));
    datas = cursor.fetchall()
    for data in datas:
        secondimg = data[18]  
    # print(headimg)
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == secondimg:
            os.remove("../shopServer/shopApp/static/myfile/"+secondimg);
    cursor.close();

    cursor=connection.cursor();
    try:
        cursor.execute("DELETE  FROM user WHERE userid = %s"%(userid))
        connection.commit();
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
            
    except Exception as e:   
         # connection.rollback();
         return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

def userManageJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    userid= request.POST["userid"]
    userid = str(userid)
    if request.FILES:
        #前台传过来的图片
        headImgs = request.FILES["headimg"];
        #随机字符串存取图片名字
        headImgsName = randomString() + ".jpg";
        print (headImgsName)
        #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
        
        cursor.execute("select headimg from user where userid='%s'" % userid)
        data = cursor.fetchall();
        if data[0][0]:
            print(data[0][0])
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,headImgsName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(headImgs.__dict__["file"].read());
        cursor.execute("update user set headimg='%s' where userid=%s"%(headImgsName , datas["userid"]))
    for key in datas:
        if key != 'userid' and datas[key] != "":
            cursor.execute("update user set %s='%s' where userid=%s"%(key , datas[key] , datas["userid"]))
    cursor.close();                   
    return HttpResponse(json.dumps(MyTool.resultOk("更新成功")) , content_type="application/json");



# 按时间获取随机字符串
def randomString():
    randomId = ""
    for i in range (0,10):  
        nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");  
        randomNum=random.randint(0,100);
        if randomNum<=10:  
            randomNum=str(0)+str(randomNum);  
        randomId=str(nowTime)+str(randomNum);
    return str(int(randomId) * 3)
def addGoodsImage(request):
    print(request.FILES);
    statusDic = "";
    cursor = connection.cursor();
    sql = "select images from goods  where goodsid='%s'" % (request.POST["goodsid"]);
    cursor.execute(sql);
    data = cursor.fetchall()
    print(data)
    temimg = data[0][0];
    print("**********&&&&&&&&&&&&")
    print(temimg)
    if not request.FILES:
        statusDic = MyTool.resultError("请选择图片");
    elif  temimg == None:
        imgs = request.FILES["imgsFile"];
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/";
        filename = os.path.join(filepath,imgsName)
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        sqlfilename = filepath+imgsName
        result=cursor.execute("UPDATE goods SET images=concat('%s','---') where goodsid='%s'" % (imgsName , request.POST["goodsid"]));
        if result == 1:
            print("插入成功");
           
            statusDic = MyTool.resultOk("添加成功")
        else :
            
            statusDic = MyTool.resultError("数据库更新失败")
    elif temimg.count("---") < 6:
        imgs = request.FILES["imgsFile"];
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/";
        filename = os.path.join(filepath,imgsName)
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        sqlfilename = filepath+imgsName
        result=cursor.execute("UPDATE goods SET images=concat('%s','%s---') where goodsid='%s'" % (temimg , imgsName , request.POST["goodsid"]));
        if result == 1:
            print("插入成功");
            
            statusDic = MyTool.resultOk("添加成功")
        else :
           
            statusDic = MyTool.resultError("数据库更新失败");
            

    else:
        statusDic = MyTool.resultOk("轮播图最多添加6个图片");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    # image=request.POST['imgsFile']
    # # image = "kkkkkkk"
    # cursor=connection.cursor()
    # result=cursor.execute("UPDATE goods SET images='%s' where goodsid='1111'"% image)
    # stadic=""
    # if result==1:
    #     stadic={"status":"ok","message":"成功"}
    # else:
    #     stadic={"status":"error","message":"失败"}
    # imgsName=randomString()+".jpg";

    # return HttpResponse(json.dumps(stadic),content_type="application/json")

        
  

    

#添加广告接口
def adManageJsonAdd(request):
                    
    adPosition=request.POST["adPosition"];
    adName=request.POST["adName"];
    adAddress=request.POST["adAddress"];
    imgs = request.FILES["images"];
    adId = randomString()

    imgsName = adId + ".jpg"; 

    try: 
        filepath = "./shopApp/static/myfile/adImgs";
        # filename = os.path.join(filepath,imgsName)
        filename = filepath + "/" + imgsName
        
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        filename.close();
    except Exception as e: 
        statusDic = MyTool.resultError("图片保存失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
   
   
   
    try:
        cursor = connection.cursor();
        sqlfilename = "static/myfile/adImgs" + "/" + imgsName
        sqlStr = "INSERT INTO ad(adid,position , imgs , adAddress , adIntroduce) VALUES ('%s','%s' , '%s' , '%s' , '%s' )" % (adId,adPosition , sqlfilename , adAddress , adName)
        result = cursor.execute(sqlStr);
        cursor.close()
        
        
        if result == 1:
            tempDic = {"imgPath":sqlfilename , "adid":adId , "position":adPosition,"adtime":"" , "address":adAddress , "introduce":adName}
            statusDic = {"status" : "ok" , "message" : "添加成功" , "data":tempDic};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic = MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

    except Exception as e: 
        statusDic = MyTool.resultError("数据库操作失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    

# 广告添加接口
def saveOneImageToServer(request):
    

    imgs = request.FILES["imgsFile"];
    imgsName = randomString() + ".jpg";
    filepath = "./shopApp/static/myfile";
    filename = os.path.join(filepath,imgsName)
    filename = open(filename , "wb");
    filename.write(imgs.__dict__["file"].read());
    filename.close();
    statusDic = {"status" : "ok" , "message" : "添加成功" , "imagePath":imgsName};
    
    
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

# 广告列表接口 兼 广告查询接口
def adManageJsonSelect(request):
    
    try:
        myData=[];
        cursor = connection.cursor();
        position = ""

        if "position" in request.POST:
            position=request.POST["position"];

        if position!="":
            sql=("select * from ad where position='%s'"%(position));
        else:
            sql="select * from ad";
        cursor.execute(sql)
        #取出数据
        datas=cursor.fetchall();
        cursor.close();
        for data in datas:
            adid=data[0];
            imgPath=data[1];
            position=data[2];   
            adtime=data[3].strftime('%Y-%m-%d %H:%M:%S')
            address=data[4]; 
            introduce=data[5]; 
            tempDic = {"imgPath":imgPath , "adid":adid , "position":position,"adtime":str(adtime) , "address":address , "introduce":introduce}
            myData.append(tempDic)
        
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}) , content_type="application/json");
    except Exception as e: 
        # raise e   
        return HttpResponse(json.dumps({'status':'error', 'message':'数据库操作失败'}), content_type="application/json");


#红包管理页面
def redpack(request):
    return render(request,"redpack.html")
#红包添加 已完成
def redpackAdd(request):
    try:
        userid=request.POST["userid"];
        redpackid = randomString()
        getpath=request.POST["getpath"];
        money=request.POST["money"];
        title=request.POST["title"];
        description=request.POST["description"];
        starttime=request.POST["starttime"];
        endtime=request.POST["endtime"];
        detail=request.POST["detail"];
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(userid,redpackid,getpath,money , title , description , starttime , endtime , detail) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s')"% (userid,redpackid,getpath,money , title , description , starttime , endtime , detail))
        
        statusDis=MyTool.resultOk("添加成功")
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        
        statusDis=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#红包添加的通用方法(非接口路由使用)
def redpackAddCurrency(userid, getpath, money):
    redpackid = randomString()
    print("********------------")
    print(redpackid,userid, getpath, money);
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(userid,redpackid,getpath,money) VALUES (%s,%s,%s,%s)"% (userid,redpackid,getpath,money))
        return True;
    except Exception as e :
        return False;

#红包删除 已完成
def redpackDelete(request):
    try:
        redpackids = request.POST["redpackids"]
        redpackids = json.loads(redpackids)
        cursor=connection.cursor();


        sqlStr = "delete FROM redpack WHERE redpackid in ("
        for deleteId in redpackids:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        result = cursor.execute(sqlStr)
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
    
    except Exception as e:
        return HttpResponse(json.dumps({'message': '红包删除接口异常,请联系服务器管理人员','status':'error'}), content_type="application/json");
    

#红包查询 已完成
def redpackApi(request):
    try:
        userid=request.POST["userid"];
        sql="SELECT * from redpack WHERE userid = '%s'" % userid 
        print(sql)
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'userid':row[0],
                'redpackid':row[1],
                'getpath':row[2],
                'money':row[3],
                'addtime':row[4].strftime('%Y-%m-%d %H:%M:%S'),
                'title':row[5],
                'description':row[6],
                'starttime':row[7],
                'endtime':row[8],
                'detail':row[9],
            }
            allOrdertables.append(ordertable)
        cursor.close()
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'message':'查询红包失败,请联系服务器人员', 'status':'error'}), content_type="application/json")

        

# 广告删除接口 韩乐天
def adManageJsonDelete(request):
    adids = []
    imgs = []

    for key in request.POST:
        if "deleteId" in key:
            adids.append(request.POST[key])
        if "deleteImg" in key:
            imgs.append(request.POST[key])

    cursor=connection.cursor();

    if len(adids) <= 0:
        return HttpResponse(json.dumps({"message":'要删除0个数据吗？' , "status":"error"}) , content_type="application/json");

    try:
        sqlStr = "delete FROM ad WHERE adid in ("
        for deleteId in adids:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        
        deleteCount = cursor.execute(sqlStr);
        cursor.close()

        if deleteCount == len(adids):
            try:
                for imgPath in imgs:
                    imgPath = imgPath.split("/")
                    imgPath = imgPath[len(imgPath) - 1]
                    removePath = "../shopServer/shopApp/static/myfile/adImgs/" + imgPath
                    os.remove(removePath);
                        
            except Exception as e:
                
                return HttpResponse(json.dumps({'message': '删除图片失败......','status':'ok'}), content_type="application/json");
            
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
     
        
    except Exception as e:
        return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");

# 商品添加接口
def goodsManageJsonAdd(request):
    datas = request.POST
    goodsid = randomString()
    sql = "INSERT INTO goods ("
    
    for item in datas:
        if item == "bigClassiData" or item == "minClassiData":
            pass;
        else :
            sql = sql + item + ","
        
    sql = sql + "standard" 
    # sql = sql[0:-1]    
    sql = sql +',goodsid' ") values (";
    goodsFenleiStr = ""
    for key in datas:
        if key == "bigClassiData" or key == "minClassiData":
            goodsFenleiStr = goodsFenleiStr + datas[key] + "-"
        else :
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        
        
    # sql = sql[0:-1]
    goodsFenleiStr = goodsFenleiStr[0:-1]
    sql = sql + "'" + goodsFenleiStr + "'"
    sql = sql +','+"'"+goodsid+"'" ")"
    try:
        cursor = connection.cursor()
        result = cursor.execute(sql)  
        cursor.close();  
        if result == 1:
            
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:
        raise e  
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

# 商品列表接口
def goodsManageJsonSelect(request):
    myData=[];
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor = connection.cursor();
    cursor.execute("SELECT * FROM goods LIMIT %d , 10"%mypage);
    datas=cursor.fetchall();
    try:
        for row in datas:
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'details':row[6],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'price':row[5],
                'goodsname':row[16],
                'stock':row[11],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d %H:%M:%S'),
                'proend':row[20].strftime('%Y-%m-%d %H:%M:%S'),
                'keywords':row[25]
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM goods")
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'goodscount':str(goodscount) }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

# 商品列表接口

# 根据分类 查询商品
def getGoodsByClassify(request):
    try:
        allGoodMes = []
        bigClassifyName = request.POST["bigClassifyName"]
        minClassifyName = request.POST["minClassifyName"]
        classifyName = bigClassifyName + "-" + minClassifyName
        sql = "SELECT * FROM goods WHERE standard like '%s'" % classifyName
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'price':row[5],
                'details':row[6],
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'stock':row[11],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'goodsname':row[16],
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
                'isinfudai':row[23],
                'isinmiaosha':row[24] , 
                'keywords':row[25]
            }
            allGoodMes.append(goods)
            
        cursor.close()
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'message':"根据分类查询商品异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json")


# 在搜索框列表上选中之后的的查询方法
def getGoodsListByQueryString (request):
    try:
        resultData = []
        queryStr = request.POST["queryStr"]
        fieldName = request.POST["fieldName"]

        cursor = connection.cursor()
        sqlStr = "select * from goods where " + fieldName + " like '%%%%%s%%%%'" % queryStr

        cursor.execute(sqlStr)
        for row in cursor.fetchall():
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'price':row[5],
                'details':row[6],
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'stock':row[11],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'goodsname':row[16],
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
                'isinfudai':row[23],
                'isinmiaosha':row[24] , 
                'keywords':row[25]
            }
            resultData.append(goods) 

        cursor.close()

        return HttpResponse(json.dumps({'data':resultData, 'status':'ok'}), content_type="application/json")
                
    except Exception as e:
        return HttpResponse(json.dumps({'message':"商品移动端列表选中后的模糊查询失败,请联系服务器管理人员", 'status':'error'}), content_type="application/json")
  



# 商品模糊查询 供移动端使用
def getGoodsBySomething(request):
    try:
        resultData = []
        queryStr = request.POST["queryStr"]
        fieldName = request.POST["fieldName"]

        cursor = connection.cursor()
        sqlStr = "select " + fieldName + " from goods where " + fieldName + " like '%%%%%s%%%%'" % queryStr

        cursor.execute(sqlStr)
        for row in cursor.fetchall():
            getString = row[0]
            # getString = getString[getString.index(queryStr):]
            resultData.append(getString) 

        cursor.close()

        # 数组去重
        resultData = list(set(resultData))

        return HttpResponse(json.dumps({'data':resultData, 'status':'ok'}), content_type="application/json")
                
    except Exception as e:
        return HttpResponse(json.dumps({'message':"商品移动端模糊查询失败,请联系服务器管理人员", 'status':'error'}), content_type="application/json")
  



# 商品列表删除接口
def goodsManageJsonDelete(request):
    try:
        goodsidsDict =  request.POST
        goodsids = goodsidsDict.getlist("goodsids")

        cursor=connection.cursor();
        result = 0
        images = goodsidsDict.getlist("images")
        for imgPath in images:
            removePath = "../shopServer/shopApp/static/myfile/" + imgPath
            os.remove(removePath);
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'有关图片删除操作异常' , "status":"error"}) , content_type="application/json");



    

    try:
        for goodsid in goodsids:
            cursor.execute("DELETE FROM lucky where goodsid = '%s'"%(goodsid))
            cursor.execute("DELETE FROM secondkill where goodsid = '%s'"%(goodsid))
            result += cursor.execute("DELETE FROM goods where goodsid = '%s'"%(goodsid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:   
        return HttpResponse(json.dumps({"message":'商品删除操作异常' , "status":"error"}) , content_type="application/json");



#商品详情列表展示
def goodsSelectByid(request):
    cursor = connection.cursor()
    goodsid = ""

    if "goodsid" in request.POST:
        goodsid = request.POST["goodsid"]

    if goodsid == "":
        sql = "SELECT * FROM goods"
    else :
        sql = "SELECT * FROM goods WHERE goodsid = '%s'" % goodsid
    allGoodMes = []
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'price':row[5],
                'details':row[6],
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'stock':row[11],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'goodsname':row[16],
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
                'isinfudai':row[23],
                'isinmiaosha':row[24] , 
                'keywords':row[25]
            }
            allGoodMes.append(goods)
            
        # 关闭连接
        cursor.close()
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'error'}), content_type="application/json")

# 商品模糊查询接口 黄景召 胡亚洲改
def commodityQuery(request):
    myData = []
    mypage = 0
    commName = ""
    timeUP = ""
    sellcountBtnUp = ""
    cursor = connection.cursor()
    if "page" in request.GET:
        mypage = (int(request.GET["page"]) - 1) * 10

    if "commName" in request.GET:
        commName = request.GET["commName"]

    if "timeUP" in request.GET:
        timeUP = request.GET["timeUP"]

    if "sellcountBtnUp" in request.GET:
        sellcountBtnUp = request.GET["sellcountBtnUp"]
 
 
    
    Status = ''
    if mypage == 0 and commName == "" and timeUP == "" and sellcountBtnUp == "":
        url = "select * from goods"
    elif timeUP == '0' and sellcountBtnUp == '0':
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName ,  Status, mypage)
    elif timeUP == '1' and sellcountBtnUp == '':
        Status = "desc"
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName , Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '0':
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by sellcount %s LIMIT %d , 10;"%(commName , Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '1':
        Status = "desc"
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by sellcount %s LIMIT %d , 10;"%(commName , Status, mypage)
    elif timeUP == '' and sellcountBtnUp == '':
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName , Status, mypage)
    elif timeUP == '0' and sellcountBtnUp == '':
        url = "SELECT * FROM goods where concat(goodsname , standard , details , shopname) like '%%%%%s%%%%' order by addtime %s LIMIT %d , 10;"%(commName , Status, mypage)
    
    
    cursor.execute(url);
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'price':row[5],
                'details':row[6],
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'stock':row[11],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                'goodsname':row[16],
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
                'isinfudai':row[23],
                'isinmiaosha':row[24] , 
                'keywords':row[25]
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM goods where goodsname like '%%%%%s%%%%'" % (commName))
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'goodscount':str(goodscount) }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");


# 商品修改列表修改接口 有待测试 黄景召
def goodsManageJsonUpdata(request):

    datas = request.POST
    tempDict = {};
    for key in datas:
        value = datas[key]
        key = key.strip("#");
        tempDict[key] = value
        

    for key in list(tempDict):
        cursor = connection.cursor()

        cursor.execute("update goods set %s='%s' where goodsid='%s'"%(key , tempDict[key] , tempDict["goodsid"]));
    
    data = {'data':'success', 'status':'ok'}
    return HttpResponse(json.dumps(data) , content_type="application/json");


# 订单添加接口 已完成
def ordertableManageJsonAdd(request):
    try:
        goodsOrders = request.POST.getlist("goodsOrders")
        goodsOrders = goodsOrders[0]
        goodsOrders = json.loads(goodsOrders)
        
        cursor = connection.cursor()
        for item in goodsOrders:
            sqlStr1 = "insert into ordertable ("
            sqlStr2 = " values ("
            for key in item:
                sqlStr1 = sqlStr1 + key + ","
                sqlStr2 = sqlStr2 + "'" + str(item[key]) + "',"

            orderId = randomString()
            sqlStr1 = sqlStr1 + "orderId,"
            sqlStr1 = sqlStr1[0:-1]
            sqlStr1 = sqlStr1 + ")"

            sqlStr2 = sqlStr2 + "'" + orderId + "',"
            sqlStr2 = sqlStr2[0:-1]
            sqlStr2 = sqlStr2 + ")"

            sqlStr = sqlStr1 + sqlStr2
            cursor.execute(sqlStr)

        cursor.close()
        
        status = json.dumps({'status':'ok','message':'asdfasdfs'})
        return HttpResponse(status, content_type="application/json")
    
    except Exception as e:
        status = json.dumps({
        'status':'error',
        'message':'订单添加接口异常,请联系服务器人员'
        })
    return HttpResponse(status, content_type="application/json")

# 订单查询列表接口 已完成
def ordertabalelistJaon(request):
    try:
        userId = request.POST["userId"]

        sqlStr = "select * from ordertable where userId = '%s'" % userId
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        for row in cursor.fetchall():
            ordertable = {
                'userId':row[0],
                'orderId':row[1],
                'goodsPrice':row[2],
                'createTime':row[3].strftime('%Y-%m-%d %H:%M:%S'),
                'status':row[4],
                'freightPrice':row[5],
                'freightRiskPrice':row[6],
                'payTime':row[7],
                'sendGoodsTime':row[8],
                'finishTime':row[9],
                'goodsId':row[10],
                'shopName':row[11],
                'goodsName':row[12],
                'goodsParams1':row[13],
                'goodsParams2':row[14],
                'goodsKeywords':row[15],
                'goodsImage':row[16],
                'goodsNumber':row[17],
                'wxOrderId':row[18],
                'goodsProPrice':row[19],
                'receiveUserName':row[20],
                'receiveUserTel':row[21],
                'receiveUserAddress':row[22],
            }
            allOrdertables.append(ordertable)
        cursor.close()
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'message':"订单查询接口异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json")
# 订单删除接口 已完成
def ordertableDelete(request):
    try:
        orderId = request.POST["orderId"]
        cursor=connection.cursor();
        result = cursor.execute("DELETE FROM ordertable WHERE orderid ='%s'" % orderId)
        cursor.close();
        if result == 1:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else:
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
    except Exception as e:
        return HttpResponse(json.dumps({'message':"订单表删除异常,请联系服务器人员", 'status':'error'}), content_type="application/json")

# 活动查询接口  有待测试
def activeManageJsonSelect(request):
    try:
        myData=[]
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM activetable ORDER BY activeid DESC")
        for data in cursor.fetchall():
            activeid=data[0]
            activedetail=data[1]
            starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
            imgs = data[3]
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
            activetitle = data[5]
            activeName = data[6]
            activePosition = data[7]
            tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");


# 活动添加接口 刘斌
def activetableManageJsonAdd(request):
    datas = request.POST
    imagesName = "None"
    #前台传过来的图片
    if request.FILES.get('imgs',False):
        print("gygygygygygygy")
        images = request.FILES["imgs"];
        #随机字符串存取图片名字
        imagesName = randomString() + ".jpg";
        #判断是否存在
        if os.path.exists("../shopServer/shopApp/static/myfile/"+imagesName)==True:
            os.remove("../shopServer/shopApp/static/myfile/"+imagesName);
        else:
            pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,imagesName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(images.__dict__["file"].read());

        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid,imgs' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"','" + imagesName +"'" ")"

    else:
        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"'" ")"
    print("************************")
    print(sql)
          
    cursor=connection.cursor()
    try:
        cursor.execute(sql)
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" %activeid)
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
        imgs = data[3]
        stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        # cursor.execute("INSERT INTO order (activeid,activetime,activedetail) VALUES (%d,%s,%s)"% (activeid,str(activetime),activedetail))
        statusDis={"status":"ok","message":"添加成功","addactive":tempDic};
        
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        raise e
       
        statusDis=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#图片上传并返回拼接地址   韩乐天
def imgUpload(request):
    uf = UserForm(request.POST,request.FILES)
    test = imagesupload();
    imgpath = test.upload(request)
    return render_to_response('test.html',{'uf':uf})
# 活动删除接口 有待测试 刘斌
def activetableManageJsonDelete(request):
    cursor=connection.cursor()
    active_id = request.GET["dataId"];
    print(active_id)
    try:
        cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % active_id)
        data = cursor.fetchall();
        if data[0][0]:
            print(data[0][0])
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        cursor.execute("DELETE FROM activetable WHERE activeid='%s'"% (active_id))
        cursor.close()
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
    except expression as identifier:
        return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
def redpack(request):
    
    return render(request,"redpack.html")

# 活动批量删除接口 胡亚洲
def activesManageJsonDelete(request):
    activeidsDict =  request.POST
    activeids = activeidsDict.getlist("activeids")
    cursor=connection.cursor();
    result = 0
    try:
        for activeid in activeids:
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % activeid)
            data = cursor.fetchall();
            if data[0][0]:
                print(data[0][0])
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            result += cursor.execute("DELETE FROM activetable where activeid = '%s'"%(activeid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");




#收藏 浏览记录 购买记录 添加接口
def favoritetableManageJsonAdd(request):
    try:
        userid = request.POST["userid"];
        goodsname = request.POST["goodsname"];
        goodsid = request.POST["goodsid"];
        goodsimage = request.POST["goodsimage"];
        goodsparams1 = request.POST["goodsparams1"];
        goodsparams2 = request.POST["goodsparams2"];
        shopname = request.POST["shopname"];
        goodsprice = request.POST["goodsprice"];
        tablename = request.POST["tablename"]  
        favoriteid = randomString()
        number = "" 
        idstring = ""
        sqlStr = ""
        if tablename == "favorite":
            idstring = "favoriteid"
        if tablename == "lookhistory":
            idstring = "lookid"  
        if tablename == "buyhistory":
            idstring = "buyid"
            number = request.POST["number"]

        cursor=connection.cursor() 
        result = cursor.execute("select goodsname from " + tablename + " where goodsid='%s'" % goodsid)

        sqlStr = "INSERT INTO " + tablename + " (" + idstring + " , userid,goodsname,goodsid , goodsimage,goodsparams1,goodsparams2 , shopname,goodsprice) VALUES('%s','%s','%s','%s','%s','%s','%s','%s' , '%s')"% (favoriteid , userid,goodsname,goodsid , goodsimage,goodsparams1,goodsparams2 , shopname,goodsprice)
        if tablename == "buyhistory":
            sqlStr = "INSERT INTO " + tablename + " (" + idstring + " , userid,goodsname,goodsid , goodsimage,goodsparams1,goodsparams2 , shopname,goodsprice , number) VALUES('%s','%s','%s','%s','%s','%s','%s','%s' , '%s' , '%s')"% (favoriteid , userid,goodsname,goodsid , goodsimage,goodsparams1,goodsparams2 , shopname,goodsprice , number) 
            

        if int(result) > 0:
            if tablename == "buyhistory":
                cursor.execute(sqlStr)
                cursor.close()
                statusDic=MyTool.resultOk("添加成功")
                return HttpResponse(json.dumps(statusDic), content_type = "application/json");
            else: 
                statusDic=MyTool.resultOk("该商品已经存在")
                cursor.close()
                return HttpResponse(json.dumps(statusDic), content_type = "application/json");
        else :
            cursor.execute(sqlStr)
            cursor.close()
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic), content_type = "application/json");
    
    
    except Exception as e :
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic), content_type = "application/json");







# 收藏 浏览记录 查询 接口
def favoritetableManageJsonSelect(request):
    try:
        myData=[]
        userid = request.POST["userid"];  
        tablename = request.POST["tablename"] 
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM %s where userid='%s'"%(tablename , userid))
        for data in cursor.fetchall():
            userid=data[0];
            favoriteid=data[1];
            goodsid =data[2]
            favtime=data[3].strftime('%Y-%m-%d %H:%M:%S');
            goodsname=data[4];
            goodsimage=data[5];
            goodsparams1 =data[6]
            goodsparams2=data[7];
            shopname=data[8];
            goodsprice =data[9]
            tempDic={"userid":userid,"favoriteid":favoriteid,"goodsid":goodsid,"favtime":favtime , "goodsname":goodsname , "goodsimage":goodsimage , "goodsparams1":goodsparams1 , "goodsparams2":goodsparams2 , "shopname":shopname , "goodsprice":goodsprice}
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}),  content_type = "application/json");      
    except Exception as e:   
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type = "application/json");

# 购物车添加接口 
def cartstableManageJsonAdd(request):   
    try: 
        cursor = connection.cursor()
        userid = request.POST["userid"] 
        number = request.POST["number"] 
        goodsid = request.POST["goodsid"] 
        goodsname = request.POST["goodsname"] 
        goodsprice = request.POST["goodsprice"] 
        goodsparams1 = request.POST["goodsparams1"] 
        goodsparams2 = request.POST["goodsparams2"] 
        goodsimage = request.POST["goodsimage"] 
        shopname = request.POST["shopname"] 
        cartsid = randomString()

        result = cursor.execute("select number from carts where goodsid='%s'" % goodsid)

        if result == 0:
            result = cursor.execute("INSERT INTO carts (userid , cartsid , number , goodsid , goodsname , goodsprice , goodsparams1 , goodsparams2 , goodsimage , shopname) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s')" % (userid,cartsid , number , goodsid , goodsname , goodsprice , goodsparams1 , goodsparams2 , goodsimage , shopname))   
            cursor.close()
            if result == 1:
                statusDis=MyTool.resultOk("添加成功")
                return HttpResponse(json.dumps(statusDis),content_type="application/json");
            else :
                statusDis=MyTool.resultError("添加失败")
                return HttpResponse(json.dumps(statusDis),content_type="application/json");
        else :
            
            cursor.execute("update carts set number = number + %d where goodsid = '%s' " % (int(number) , goodsid))
            cursor.close()
            statusDis=MyTool.resultOk("累加成功")
            return HttpResponse(json.dumps(statusDis),content_type="application/json");  
            
        
       
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"购物车添加操作失败，请联系服务器人员","status":"error"}),content_type="application/json")



#购物车 浏览记录 收藏表 批量删除接口
def cartstableManageJsonDelete(request):
    try:
        cartsids = request.POST["ids"]
        tablename = request.POST["tablename"]
        idstring = ""
        if tablename == "carts":
            idstring = "cartsid"
        if tablename == "favorite":
            idstring = "favoriteid"
        if tablename == "lookhistory":
            idstring = "lookid"


        cartsids = json.loads(cartsids)
        cursor=connection.cursor()
        sqlStr = "delete from " + tablename + " where " + idstring + " in ("
        for item in cartsids:
            sqlStr = sqlStr + "'" + item + "',"
        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        cursor.execute(sqlStr)
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")


#购物车修改数量接口   已经完成
def cartstableManageJsonUpdate(request):
    try:
        cursor = connection.cursor();
        cartsid = request.POST["cartsid"];   
        number = request.POST["number"]
        result = cursor.execute("update carts set number='%s' where cartsid='%s'"%(number , cartsid))
        cursor.close();
        if result == 1:
            return HttpResponse(json.dumps({"message":"修改成功","status":"ok"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"购物车查询操作失败，请联系服务器人员","status":"error"}),content_type="application/json")



#购物车查询接口  已经完成
def cartstableManageJsonSelect(request):  
    try:
        cursor = connection.cursor()
        userid = request.POST["userid"]
        myData = []
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM carts WHERE userid='%s'" % userid)
        datas = cursor.fetchall()
        cursor.close()
        for data in datas:
            userid = data[0];
            cartsid = data[1];
            number = data[2];
            goodsid = data[3];
            goodsname = data[4];
            goodsprice = data[5];

            goodsparams1 = data[6];
            goodsparams2 = data[7];
            goodsimage = data[8];
            shopname = data[9];
            tempDic = {"cartsid":cartsid , "number":number , "goodsid":goodsid , "userid":userid , "goodsname":goodsname , "goodsprice":goodsprice , "goodsparams1":goodsparams1 , "goodsparams2":goodsparams2 , "goodsimage":goodsimage , "shopname":shopname }
            myData.append(tempDic)
        return HttpResponse(json.dumps(myData) , content_type="application/json");
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"购物车查询操作失败，请联系服务器人员","status":"error"}),content_type="application/json")







#添加抽奖余额接口
def drawJsonAdd(request):  
    cursor = connection.cursor() 
    userid = request.POST["userid"];
    drawmoney = request.POST["drawmoney"];
    drawdetail = request.POST["drawdetail"];
    username = "11111"
    drawid = randomString();
    try:
        cursor.execute("INSERT INTO draw (userid , drawmoney , username , drawdetail , drawid) VALUES ('%s' , '%s' , '%s' , '%s' , '%s')" % (userid , drawmoney , username , drawdetail , drawid))
        statusDis=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#删除抽奖余额接口
def drawJsonDel(request):
    cursor = connection.cursor()
    userid = request.POST["userid"];
    drawid = request.POST["drawid"];   
    try:
        cursor.execute("DELETE FROM draw WHERE drawid=\"%s\""%drawid)
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#更新抽奖接口
def drawJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    try:
        for key in list(datas):
            cursor.execute("update draw set %s='%s' where userid='%s'"%(key , datas[key] , datas["userid"]))
            statusDis=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
# 查询抽奖余额接口
def drawJsonQuery(request):
    cursor = connection.cursor()
    userid = request.POST["userid"]
    myData = []
    try:
        cursor.execute('SELECT * FROM draw WHERE userid=\"%s\"' % userid)
        datas = cursor.fetchall()
        print(datas)
        for data in datas:
            userid = data[0];
            drawmoney = data[1];
            drawtime = data[2].strftime('%Y-%m-%d %H:%M:%S');
            username = data[3];
            drawid = data[4];
            drawdetail = data[5];
            tempDic = {"userid":userid , "drawmoney":drawmoney , "drawtime":drawtime ,"username":username , "drawid":drawid , "drawdetail":drawdetail}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");
    except:
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    pass
# 福袋管理页面 胡亚洲
def luckyManage(request):
    return render(request , "luckyManage.html");
# 福袋模查询接口
def luckyManageJsonQuery(request):
    myData = []
    timeUP = "0"
    commName = ""
    cursor = connection.cursor()
    if "commName" in request.GET:
        commName = request.GET["commName"]

    if "timeUp" in request.GET:
        timeUP = request.GET["timeUp"]
    timeStatus = "desc"
    if timeUP == '1':
        timeStatus = ""

    sqlStr = ""
    
    if commName == "":
        sqlStr = "SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid order by lucky.uptime %s" % timeStatus
    else :
        sqlStr = "SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsname like '%%%%%s%%%%' order by lucky.uptime %s"%(commName, timeStatus)
    
    cursor.execute(sqlStr);
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = row[5].strftime('%Y-%m-%d %H:%M:%S')
            except:
                uptime = "未知"
            lucky = {
                'luckyid':row[0],
                'goodsid':row[1],
                'goodsname':row[2],
                'counts':row[3],
                'price':row[4],
                'uptime':uptime,
            }
            myData.append(lucky);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:  
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");
# 福袋列表删除接口 胡亚洲
def luckyManageJsonDelete(request):
    luckyidsDict =  request.POST
    luckyids = luckyidsDict.getlist("luckyids")
    goodsids = luckyidsDict.getlist("goodsids")
    cursor=connection.cursor();
    result = 0
    try:
        for (myindex , luckyid) in enumerate(luckyids):
            result += cursor.execute("DELETE FROM lucky where luckyid = '%s'"%(luckyid))
            cursor.execute("UPDATE goods SET isinfudai = 'false' WHERE goodsid = '%s'" % goodsids[myindex])
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");



# 福袋修改列表修改接口 胡亚洲
def luckyManageJsonUpdata(request):
    print(request.POST)
    num=request.POST["num"];
    luckyid=request.POST["luckyid"]
    try:
        cursor = connection.cursor()
        cursor.execute("update lucky set counts='%s' where luckyid='%s'"%(num , luckyid))
        data = {'data':'success', 'status':'ok'}
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'修改失败' , "status":"error"}) , content_type="application/json");
# 福袋添加接口 胡亚洲
def luckyManageJsonAdd(request):
    try:
        goodsName = request.POST["goodsName"]
        goodsId = request.POST["goodsId"]
        counts = request.POST["counts"]
        luckyid = randomString()
        print(luckyid, goodsName, counts)
        cursor = connection.cursor()
        sql = "INSERT INTO lucky (luckyid , goodsname , counts , goodsid) VALUES('%s','%s','%s','%s')" % (luckyid, goodsName, counts , goodsId)
        result = cursor.execute(sql)
        
        if result == 1 :
            # 将商品的状态改变了 (isinfudai)
            cursor.execute("UPDATE goods SET isinfudai = 'true' WHERE goodsid = '%s'" % goodsId)
            cursor.close()

            statusDic = {"status" : "ok" , "message" : "添加成功"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            cursor.close()
            statusDic = {"status" : "error" , "message" : "添加失败"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");


# 评论查询(通过用户id和商品id) 胡亚洲
def commentJsonQuery(request):
    myData = []

    userid = ""
    goodsid = ""
    
    if "userid" in request.GET:
        userid = request.GET["userid"]

    if "goodsid" in request.GET:
        goodsid = request.GET["goodsid"]

    sqlStr = "select * from comment"
    # 查询所有评论
    if userid == "" and goodsid == "":
        pass

    # 按照商品id查询评论
    if userid == "" and goodsid != "":
        sqlStr = "select * from comment where goodsid = '%s'" % goodsid
    
    # 按照用户id查询评论
    if userid != "" and goodsid == "":
        sqlStr = "select * from comment where userid = '%s'" % userid

    # 按照用户id和商品id来查找评论
    if userid != "" and goodsid != "":
        sqlStr = "select * from comment where userid = '%s' and goodsid = '%s'" % (userid , goodsid)



    cursor = connection.cursor()
    luckycount = cursor.execute(sqlStr);
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = row[4].strftime('%Y-%m-%d %H:%M:%S')
            except:
                uptime = "未知"
            comment = {
                'commentid':row[0],
                'goodsid':row[1],
                'userid':row[2],
                'comment_text':row[3],
                'uptime':uptime,
            }
            myData.append(comment);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(luckycount) }), content_type="application/json")
    
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

# 评论删除接口 胡亚洲
def commentJsonDelete(request):
    commentidsDict =  request.POST
    commentids = luckyidsDict.getlist("commentids")
    cursor=connection.cursor();
    result = 0
    try:
        for commentid in commentids:
            result += cursor.execute("DELETE FROM comment where commentid = '%s'"%(commentid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

# 评论添加接口 胡亚洲
def commentJsonAdd(request):
    try:
        commentid = randomString()
        goodsid = request.POST["goodsid"]
        userid = request.POST["userid"]
        comment_text = request.POST["comment_text"]
        cursor = connection.cursor()
        sql = "INSERT INTO comment (commentid , goodsid , userid , comment_text) VALUES('%s','%s','%s','%s')" % (commentid, goodsid, userid, comment_text)
        result = cursor.execute(sql)
        if result == 1 :
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            statusDic=MyTool.resultError("添加失败");
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

#购物车获取数据接口
def cartstableManageJsonGain(request):
    cursor = connection.cursor()
    name = "liu";
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s_carts" % (name));
    datas = cursor.fetchall()
    for data in datas:
        cartsid = data[0];
        number = data[1];
        goodsid = data[2];
        userid = data[3];
        tempDic = {"cartsid":cartsid , "number":number , "goodsid":goodsid , "userid":userid }
        myData.append(tempDic)

    return HttpResponse(json.dumps(myData) , content_type="application/json");
#添加地址接口
def addAddress(request):
    try:
        cursor = connection.cursor()
        addid = randomString()
        userid = request.POST["userid"]
        username = request.POST["username"]
        tel = request.POST["tel"]
        address = request.POST["address"]
        mailcode = request.POST["mailcode"]
        flag = request.POST["flag"]

        
        result = cursor.execute("INSERT INTO address (addid , userid , username , tel , address , mailcode , flag) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' )" % (addid , userid , username , tel , address , mailcode , flag))
        if result == 1:
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else :
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");

#删除地址接口
def delAddress(request):
    cursor = connection.cursor()
    addid = request.POST["addid"]
    
    try:
        cursor.execute("DELETE FROM address WHERE addid='%s'" % addid)
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#更新地址接口
def updateAddress(request):
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update address set %s='%s' where addid='%s'"%(key , datas[key] , datas["addid"]))
            statusDis=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")


#查找地址接口
def findAddress(request):
    cursor = connection.cursor()
    userid = request.POST["userid"]

    myData = []
    try:
        cursor.execute('SELECT * FROM address WHERE userid=\"%s\"' % userid)
        datas = cursor.fetchall()
        cursor.close()
        for data in datas:
            addid = data[0]
            userid = data[1]
            username = data[2]
            tel = data[3]
            address = data[4]
            mailcode = data[5]
            tempDic = {"addid":addid , "userid":userid , "username":username , "tel":tel , "address":address , "mailcode":mailcode}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");

    except:
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
 


#删除余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def delMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        sql = "delete from remainmoney where userId='%s'" % userid;
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("删除成功")
        else:
            statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#添加余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def addMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        money = request.GET["money"];
        sql = "insert into remainmoney (userId , money) values('%s','%s')" % (userid , money);
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("添加成功")
        else:
            statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
#更新余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def updateMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        money = request.GET["money"];
        sql = "update remainmoney set money='%s' where userId='%s'" % (money ,userid);
        cursor = connection.cursor();
        result = cursor.execute(sql);
        if result:
            statusDis=MyTool.resultOk("修改成功")
        else:
            statusDic=MyTool.resultError("修改失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
#查询余额接口实现，获取数据测试用GET ，具体情况具体使用  王贺
def findMoney(request):
    statusDic = "";
    if request.GET :
        userid = request.GET["userId"];
        print (userid);
        sql = "select * from remainmoney where userId='%s'" % userid;
        print(sql);
        cursor = connection.cursor();
        datas = cursor.execute(sql);
        myData = [];
        datas = cursor.fetchall()
        print (datas);
        if datas:
            for data in datas:
                userid = data[0];
                money = data[1];
                tempDic = {"userId":userid , "money":money}
                myData.append(tempDic)
            statusDic = {"data" : myData,"status" : "ok", "message" : "查找成功"};
        else:
            statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    else:
         
        statusDic=MyTool.resultError("没有数据");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#查询用户留言接口
def leaveMessage(request):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM message')
    a = cursor.fetchall()
    print(a)
    cursor.close()
    imgDic = []
    for i in a:
        aaa = {"goodsid":i[0] , "userid":i[1] , "leavemessage":i[2]}
        imgDic.append(aaa)
    return HttpResponse(json.dumps(imgDic) , content_type = "application/json")

#增加用户留言接口
def addLeaveMessage(request):
    data = request.POST
    goodsid = data["goodsid"]
    userid = data["userid"]
    leavemessage = data["leavemessage"]
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # goodsid = "2017121519245103"
    # userid = "2017121519245103"
    # leavemessage = "啥的感觉爱仕达将刷机大师"
    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO message(goodsid , userid , leavemessage)VALUES('%s' , '%s' , '%s')"%(goodsid , userid , leavemessage))
    cursor.close()
    if result == 1:
         statusDis=MyTool.resultOk("留言添加成功")
    else :
        statusDic=MyTool.resultError("留言添加失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

#删除用户留言接口
def deleLeaveMessage(request):
    data = request.POST
    goodsid = data["goodsid"]
    userid = data["userid"]
    # goodsid = "2017121115433480"
    # userid = "2017121517150701"
    # print("***********************8")
    cursor = connection.cursor()
    sql = " delete from message where goodsid = '"+goodsid+"' and userid = '" + userid +"'"
    result = cursor.execute(sql)
    cursor.close() 
    if result == 0:
        statusDis=MyTool.resultOk("留言删除成功")
    else :
        statusDic=MyTool.resultError("留言删除失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

#添加分享接口 已完成
def addShare(request):
    try:
        goodsid = request.POST["goodsid"]
        userid = request.POST["userid"]
        sharepath = request.POST["sharepath"]
        goodsname = request.POST["goodsname"]
        goodsprice = request.POST["goodsprice"]
        goodsimage = request.POST["goodsimage"]
        goodsparams1 = request.POST["goodsparams1"]
        goodsparams2 = request.POST["goodsparams2"]

        shareid = randomString()

        cursor = connection.cursor()
        result = cursor.execute("INSERT INTO share (shareid , goodsid , userid , sharepath , goodsname , goodsprice , goodsimage , goodsparams1 , goodsparams2) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s')" % (shareid , goodsid , userid , sharepath , goodsname , goodsprice , goodsimage , goodsparams1 , goodsparams2))
        cursor.close()
        if result == 1:
            statusDis=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
        else :
            statusDis=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("分享添加异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#删除分享接口 已完成
def delShare(request):
    try:
        cursor = connection.cursor()
        shareid = request.POST["shareid"]
        cursor.execute("DELETE FROM share WHERE shareid='%s'" % shareid)
        cursor.close()
        statusDis=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("分享删除异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

# 分享列表接口 已完成
def findShare(request):
    try:
        cursor = connection.cursor()
        userid = request.POST["userid"]
        myData = []
        cursor.execute("SELECT * FROM share WHERE userid='%s'" % userid)
        datas = cursor.fetchall()
        cursor.close()
        for data in datas:
            shareid = data[0]
            goodsid = data[1]
            userid = data[2]
            sharepath = data[3]
            sharetime = data[4]
            if sharetime != None:
                sharetime = sharetime.strftime('%Y-%m-%d %H:%M:%S') 
            goodsname = data[5]
            goodsprice = data[6]
            goodsimage = data[7]
            goodsparams1 = data[8]
            goodsparams2 = data[9]
            tempDic = {"shareid":shareid , "goodsid":goodsid , "userid":userid , "sharepath":sharepath , "sharetime":sharetime , "goodsname":goodsname , "goodsprice":goodsprice , "goodsimage":goodsimage , "goodsparams1":goodsparams1 , "goodsparams2":goodsparams2}
            myData.append(tempDic)

        return HttpResponse(json.dumps({"data":myData , "status":"ok"}) , content_type="application/json");

    except:
        statusDic=MyTool.resultError("分享查询异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");


#订单分页
def orderSpilit(request):
    print("******************************************")
    myData = []
    cursor = connection.cursor()
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor.execute("SELECT * FROM ordertable LIMIT %d , 10;" % mypage);
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = {
                'userid':row[0],
                'orderid':row[1],
                'price':row[2],
                'ordertime':row[3].strftime('%Y-%m-%d %H:%M:%S'),
                'status':row[4]
            }
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM ordertable")
        ordercount  = cursor.fetchall();
        ordercount = ordercount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'ordercount':str(ordercount)}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error' , 'ordercount':str(ordercount)}), content_type="application/json");

#积分添加接口
def scoreAdd(request):
    userid = "1111"
    scoreid = "2221"
    scoretime = "3331"
    scorecount = "4441"
    getpath = "5551"
    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO score(userid , scoreid , scoretime , scorecount , getpath) VALUES ('%s' , '%s' , '%s' ,'%s' ,'%s')" % (userid , scoreid , scoretime , scorecount , getpath))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#积分删除接口
def scoreDelete(request):
    scoreid = request.POST["scoreid"]
    try:
        cursor.execute("DELETE * FROM score WHERE %s" %(scoreid))
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

#积分查询接口
def scoreSelect(request):
    userid = request.POST["userid"]
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT (userid , scoreid , scoretime , scorecount ,getpath) FROM score WHERE userid = %s" %userid)
    try:
        for data in cursor.fetchall():
            userid=data[0]
            scoreid=data[1]
            scoretime=data[2]
            scorecount = data[3]
            getpath = data[4]
            tempDic={"userid":userid,"scoreid":scoreid,"scoretime":scoretime,"scorecount":scorecount,"getpath":getpath}
            myData.append(tempDic)
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

# 购买历史添加接口
def buyhistoryAdd(request):

    userid=goodsid=goodsname=buytime=price=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    cursor = connection.cursor()
    result = cursor.execute("INSERT INTO buyhistory(userid , goodsid , goodsname , buytime , price) VALUES ('%s' , '%s' , '%s' ,'%s' ,'%s')" % (userid , goodsid , goodsname , buytime , price))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#购买记录删除接口
def buyhistoryDelete(request):
    goodsid = request.POST["goodsid"]
    try:
        cursor.execute("DELETE * FROM buyhistory WHERE %s" %(goodsid))
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");

# #积分查询按钮 吕建威
# def scoreSelect(request):

# #积分查询按钮 吕建威
# def scoreSelect(request):
#购买记录查询接口
def buyhistorySelect(request):
    userid = request.POST["userid"]
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT * FROM buyhistory WHERE userid = %s" %userid)
    try:
        for data in cursor.fetchall():
            userid=data[0]
            goodsid=data[1]
            goodsname=data[2]
            buytime = data[3]
            price = data[4]
            tempDic={"userid":userid,"goodsid":goodsid,"goodsname":goodsname,"buytime":buytime,"price":price}
            myData.append(tempDic)
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");

#好友列表查询功能
def friendslistManageJsonSelect(request):
    # friendslistid = request.friendsList["friendslistid"]
    friendslistid = "11"
   
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM friendsList WHERE friendslistid='%s'" % (friendslistid))
    for data in cursor.fetchall():
        friendslistid = data[0];
        userid = data[1];
        friendid = data[2];
        setuptime = data[3].strftime('%Y-%m-%d %H:%M:%S');
    
        tempDic = {"friendslistid":friendslistid , "userid":userid , "friendid":friendid , "setuptime":setuptime}
        myData.append(tempDic)
    cursor.close()
    return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
def settings(request):
    return render(request,"setting.html")
def settingsApi(request):
    sql="";
    if request.POST and (request.POST["settingid"]!=""):
        print("666666666666666666666666666666666")
        settingid=request.POST["settingid"];     
        sql="update settingtable redmoney='%s',rebatepercent='%s',rebatevalue='%s' WHERE settingid='%s'"%(redmoney,rebatepercent,rebatevalue,settingid);
     
    else:
        sql = "SELECT * FROM settingtable";   
    # try:
    print(sql)
    allOrdertables = [];
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        ordertable = {
            'settingid':row[0],
            'redmoney':row[1],
            'rebatepercent':row[2],
            'rebatevalue':row[3],
        }
        allOrdertables.append(ordertable)
    cursor.close()
    return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")

def settingsAdd(request):
    settingid=request.POST["settingid"];
    redmoney=request.POST["redmoney"];
    rebatepercent=request.POST["rebatepercent"];
    rebatevalue=request.POST["rebatevalue"];
    print(settingid,redmoney,rebatevalue);
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO settingtable(settingid,redmoney,rebatepercent,rebatevalue) VALUES (%s,%s,%s,%s)"% (settingid,redmoney,rebatepercent,rebatevalue))
        statusDis=MyTool.resultOk("添加成功");
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e :
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
def settingsUpdate(request):   
    cursor = connection.cursor()
    
    datas = request.POST
    settingid= request.POST["settingid"]
    settingid = str(settingid)
    for key in datas:
        if key != 'settingid' and datas[key] != "":
            cursor.execute("update settingtable set %s='%s' where settingid=%s"%(key , datas[key] , datas["settingid"]))
    cursor.close();                   
    return HttpResponse(json.dumps({"message":"更新成功" , "status":"ok"}) , content_type="application/json");

#base页面消息接口
def guestbookSelect(request):  
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guestbook")
    data = cursor.fetchall()
    dataArr = []
    for i in data:
        userid = i[1]
        cursor.execute("SELECT * FROM user WHERE userid= %s "%(userid))
        userA = cursor.fetchall()
        userName = userA[0][1]
        userHeading = userA[0][2]
        ss = {"guestbookid":i[0] , "userid":i[1] , "leavemessage":i[2] , "leavtime":str(i[3]) , "status":i[4] , "username":userName , "userHeading":userHeading}
        dataArr.append(ss)
    cursor.close();
                     
    return HttpResponse(json.dumps({"data":dataArr , "status":"ok"}) , content_type="application/json");


def leavingMessage(request):
    return render(request , "leavingMessage.html");

#获取session接口
def getSession(request):
    is_login = request.session.get('IS_LOGIN',False)
    # print(is_login)

    print("获取缓存......");
    print(request.session.__dict__)

    return HttpResponse(json.dumps({"data":is_login , "status":"ok"}) , content_type="application/json");
#设置session接口
def setSession(request):
    request.session['IS_LOGIN'] = False
    is_login = request.session.get('IS_LOGIN')

    print("清空缓存......");
    print(request.session.__dict__)
    return HttpResponse(json.dumps({"status":"ok"}) , content_type="application/json");
#获取当前时间
def getdatatime(request):
    secondkill = "";
    string = '2014-01-08 11:59:58'
    time1 = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
    starttime = request.POST["starttime"];
    stoptime = request.POST["stoptime"]
    a = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    starttime= datetime.datetime.strptime(starttime,"%Y-%m-%d %H:%M:%S")  
    stoptime = datetime.datetime.strptime(stoptime,"%Y-%m-%d %H:%M:%S")  
    nowtime= datetime.datetime.strptime(a,"%Y-%m-%d %H:%M:%S")

    nowtime = int((nowtime - time1).seconds);
    starttime = int((starttime-time1).seconds);
    stoptime = int((stoptime - time1).seconds);
    startleng = nowtime - starttime;
    stopleng = nowtime - stoptime;
    if startleng < 0:
        secondkillstatus = 0;#未开始
    if startleng >=0 and stopleng <0:
        secondkillstatus = 1;#正进行
    if stopleng >=0:
        secondkillstatus = 2;#以结束


    return HttpResponse(json.dumps({"status":"ok" , "datatime":secondkillstatus}) , content_type="application/json");



#秒杀
def secondkillManageJsonAdd(request):
    cursor = connection.cursor();
    killid = randomString();
    goodsid = request.POST["goodsid"];
    goodsname = request.POST["goodsname"];
    # goodstatus = request.POST["goodstatus"];
    goodstatus = '0'
    starttime = request.POST["starttime"];
    
    stoptime = request.POST["stoptime"]
    result = cursor.execute("INSERT INTO secondkill(killid , goodsid , goodstatus,starttime, stoptime,goodsname) VALUES ('%s' , '%s' ,'%s' , '%s' , '%s','%s')" % (killid , goodsid , goodstatus, starttime ,stoptime,goodsname))
    try:
        if result == 1:
            statusDis=MyTool.resultOk("添加成功");
            cursor.execute("UPDATE goods SET isinmiaosha = 'true' WHERE goodsid = '%s'" % goodsid)
            cursor.close()
            return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except Exception as e:
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
def secondkillManageJsonSelect(request):
    cursor=connection.cursor()
    myData=[]
    cursor.execute("SELECT killid , goodsid , goodstatus ,starttime ,  stoptime FROM secondkill")
    try:
        print("*********")
        for data in cursor.fetchall():
            killid=data[0]
            goodsid=data[1]
            goodstatus=data[2]
            starttime = data[3].strftime('%Y-%m-%d %H:%M:%S') 
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S');
            tempDic={"killid":killid,"goodsid":goodsid,"goodstatus":goodstatus,"starttime":starttime, "stoptime":stoptime}
            myData.append(tempDic)
        cursor.close()
        print(tempDic)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");
def secondkillManageJsonDelete(request):
    killid = request.POST["killid"];
    goodsid = request.POST["goodsid"];
    
    cursor=connection.cursor()
    try:
        cursor.execute("DELETE FROM secondkill where killid = %s" %killid)
        cursor.execute("UPDATE goods SET isinmiaosha = 'false' WHERE goodsid = '%s'" % goodsid)
        statusDis=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
    except:
        
        statusDic=MyTool.resultError("秒杀删除异常操作....")
        return HttpResponse(json.dumps(statusDis),content_type="application/json");
#秒杀分页 韩乐天
def secondkillcommodityQuery(request):
    print("-------------------")
    try:
        myData=[];
        mypage = (int(request.POST["page"]) - 1) * 8
        print(mypage)
        cursor = connection.cursor();
        #以八条数据为一页返回第mypage页,并且按时间排序
        cursor.execute("SELECT * FROM secondkill  LIMIT %d , 8"%mypage);
        #取出数据
        datas=cursor.fetchall();
        for data in datas:
            killid = data[0];
            goodsid = data[1];
            goodstatus = data[2];
            starttime = data[3].strftime('%Y-%m-%d %H:%M:%S');
            stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S');
            goodsname = data[5];
            tempDic = {"killid":killid, "goodsid":goodsid , "goodstatus":goodstatus , "starttime":starttime , "stoptime":stoptime ,"goodsname":goodsname}
            myData.append(tempDic)
        #查出总共有多少条数据
        cursor.execute("SELECT COUNT(*) FROM secondkill")
        adcounts  = cursor.fetchall();
        adcounts = adcounts[0][0];
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'adcounts':str(adcounts)}) , content_type="application/json");
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'adcounts':'0'}), content_type="application/json");
def secondkillManageJsonUpdata(request):
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update secondkill set %s='%s' where killid='%s'"%(key , datas[key] , datas["killid"]))
            statusDis=MyTool.resultOk("修改成功");
        return HttpResponse(json.dumps(statusDis) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
def secondkillManageJsonstock(request):
    killid = request.POST["killid"];
    cursor = connection.cursor();
    
    print(killid)
    try:
        cursor.execute("select stock from goods where goodsid = (select goodsid from secondkill where killid = '%s')"%killid);
        data = cursor.fetchall();
        stock = data[0][0];
        print(stock)
        cursor.close();
        return HttpResponse(json.dumps({'data':stock, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"没有该商品", 'status':'error'} , content_type="application/json"))
def secondkillAddgoodsidintogoods(request):
    goodsid = request.POST['goodsid'];
    cursor = connection.cursor();
    killid = randomString();
    print(goodsid)
    try:
        sql = "INSERT INTO secondkill(killid,goodsid) VALUES ('%s','%s')" %  (killid,goodsid) ;
        cursor.execute(sql);
        cursor.close();
        return HttpResponse(json.dumps({'message':'添加成功', 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"添加失败", 'status':'error'}) , content_type="application/json")
# 快递查询接口  测试版   （陈云飞）
def express(request):

    # print(datas)
    # return HttpResponse("datas")
    NO = request.POST["NO"];
    company = request.POST["company"];
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/index"
    print(type(company))
    params = {
        "com" : company, #需要查询的快递公司编号
        "no" : NO, #需要查询的订单号
        "key" : appkey, #应用APPKEY(应用详细页查询)
        "dtype" : "json", #返回数据的格式,xml或json，默认json
    
    }
    params = urlencode(params)
    print(params)    
    f = urllib.request.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    print(res)
    error_code = res["error_code"]    
    if error_code == 0:
        #成功请求
        resultDic = (res['result'])
        print(resultDic)
        return HttpResponse(json.dumps(resultDic) , content_type="application/json");
    else:
        return HttpResponse(json.dumps({"error_code":res["error_code"] , "reason":res["reason"]}) , content_type="application/json");

#查询快递公司编号接口  测试用 （陈云飞）
def expressCompany(request):
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/com";
    params = {
        "key":appkey
    }
    params = urlencode(params)
    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            return HttpResponse(res["result"])
        else:
            return HttpResponse("%s:%s" % (res["error_code"],res["reason"]))
    else:
        return HttpResponse("request api error")

#发送短信接口  测试用  （陈云飞）
def shortMsgFromName(request):
    username = request.POST["username"];
    cursor = connection.cursor();
    cursor.execute('SELECT * FROM manager WHERE username = "%s"' % username)
    datas = cursor.fetchall();
    for i in datas:
        phone = i[2];
        p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
        match = p.match(phone)
        if match:  

            sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
            appkey = '0f2f46d95cfe854988012bf5a1da65cf';
            mobile = phone;
            tpl_id = "56951";
            code = str(random.randint(0,999999));
            tpl_value = '#code#='+code;
            params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
                    (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
        
            wp =urllib.request.urlopen(sendurl+"?"+params)
            content = wp.read() #获取接口返回内容
        
            result = json.loads(content)
            error_code = result['error_code']
            if error_code == 0:
                #发送成功
                smsid = result['result']['sid']
                statusDic = {"status":"ok" , "smsid":smsid}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
            else: 
                #发送失败
                statusDic = {"status":"error" , "reason":result['reason']}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else:
            
            statusDic=MyTool.resultError("手机号码格式出错")
            return HttpResponse(json.dumps(statusDic) , content_type="application/json")


    

#发送短信接口  测试用  （陈云飞）
def shortMsgFromPhone(request):
    phone = request.POST["phone"]
    p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
    match = p.match(phone)
    if match:
        sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
        appkey = '0f2f46d95cfe854988012bf5a1da65cf';
        mobile = phone;
        tpl_id = "56951";
        code = str(random.randint(0,999999));
        tpl_value = '#code#='+code;
        params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
        (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
            
        wp =urllib.request.urlopen(sendurl+"?"+params)
        content = wp.read() #获取接口返回内容
            
        result = json.loads(content)
        error_code = result['error_code']
        if error_code == 0:
            #发送成功
            smsid = result['result']['sid']
            statusDic = {"status":"ok" , "smsid":smsid}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else: 
            #发送失败
            statusDic = {"status":"error" , "reason":result['reason']}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
    else:
        
        statusDic=MyTool.resultError("手机号码格式出错")
        return HttpResponse(json.dumps(statusDic) , content_type="application/json")

#活动修改接口
# def activetableManageJsonchange(request):     
#     imgs = request.FILES["sb"];
#     activeid = request.POST["activeid"]
#     activeidw = randomString()
#     imgsName = activeidw + ".jpg";
#     imagePath = imgsName;
#     filepath = "./shopApp/static/myfile";
#     filename = os.path.join(filepath,imgsName)
#     filename = open(filename , "wb");
#     filename.write(imgs.__dict__["file"].read());
#     filename.close();
#     sqlfilename = imgsName
#     print(sqlfilename)
#     cursor = connection.cursor();
#     result = cursor.execute("UPDATE activetable SET imgs='%s' WHERE activeid='%s'" % (sqlfilename , activeid));
#     statusDic = "";
#     if result == 1:
#         statusDic = {"status" : "ok" , "message" : "编辑成功" };
#     else :
#         statusDic = {"status" : "error" , "message" : "添加失败"};
#     return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

#活动修改接口
def activetableManageJsonchange(request):
    try:
        print("activetableManageJsonchange ******** ")
        datas = request.POST
        # print(datas)
        cursor=connection.cursor();
        if request.FILES:
            #前台传过来的图片
            Imgs = request.FILES["imgs"];
            print("*-*-*-*-*-*-*-*", Imgs)
            #随机字符串存取图片名字
            ImgsName = randomString() + ".jpg";
            print (ImgsName)
            #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
            
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % datas["activeid"])
            data = cursor.fetchall();
            if data[0][0]:
                print(data[0][0])
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            filepath = "./shopApp/static/myfile/";
            #路径组合
            filepath = os.path.join(filepath,ImgsName)
            #在路径中创建图片名字
            fileobj = open(filepath , "wb");
            #并把前端传过来的数据写到文件中
            fileobj.write(Imgs.__dict__["file"].read());
            cursor.execute("update activetable set imgs='%s' where activeid=%s"%(ImgsName , datas["activeid"]))
        for key in list(datas):
            if key != "imgs":
                cursor.execute("update activetable set %s='%s' where activeid='%s'"%(key , datas[key] , datas["activeid"]))
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" % datas["activeid"])
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=data[2].strftime('%Y-%m-%d %H:%M:%S')
        imgs = data[3]
        stoptime = data[4].strftime('%Y-%m-%d %H:%M:%S')
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        data = {'data':'success', 'status':'ok','addactive':tempDic}
        cursor.close();
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e :
        cursor.close();
        raise e
        statusDis={'data':'error', 'status':'error'};
        return HttpResponse(json.dumps(statusDis),content_type="application/json");


def audioToStr(request):
     return render(request , "audioToStr.html");


def audioToStrApi(request):
    statusDis = {};
    if request.POST["audio"]:
        mydata = request.POST["audio"];
        mydata = mydata.split(",")
        mydata = mydata[1];
        mybyte = base64.b64decode(mydata);
        filepath ="./shopApp/static/myfile/audio.wav";
        myfile = open(filepath , "wb");
        myfile.write(mybyte);
        myfile.close();
        allPath = os.path.abspath(filepath);
        tmpAllPath = allPath.replace("audio","Str")
        if os.path.exists(allPath):
            print (allPath);
            cmd = "ffmpeg -i %s -ar 16000 -ac 1 %s" % (allPath ,tmpAllPath);
            # cmd = 'ffmpeg'
            print (cmd);
            ret = subprocess.run(cmd , shell=True);
            if os.path.exists(tmpAllPath):
                myfile = open(tmpAllPath , "rb");
                audiobyte = myfile.read();
                myfile.close();
                APP_ID = '10573104'
                API_KEY = 'iGPGdtRjwadhpRdsG89iSIrp'
                SECRET_KEY = '1c169dc662f8bfdf88f73fe3e8a1940d'
                aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
                result = aipSpeech.asr(audiobyte, 'wav', 16000, {'lan': 'zh',});
                os.remove(tmpAllPath);
                print (result);
                if result["err_no"] == 0:
                    result = result["result"][0];
                    statusDis = {"status":"ok" , "result":result};
                else:
                    statusDis = {"status":"error" , "result":"请说普通话"};
            else:
                statusDis = {"status":"error" , "result":"数据转换失败"};
        else:
            statusDis = {"status":"error" , "result":"数据写入失败"};
    else:
        statusDis = {"status":"error" , "result":"没有接受到数据"};
    return HttpResponse(json.dumps(statusDis) , content_type = "application/json");



#留言删除接口
def leavingMessDelete(request):
    cursor=connection.cursor();
    data = request.POST
    data = data.getlist("data[]")
    for key in data:
        result = cursor.execute("UPDATE guestbook SET status='read' WHERE guestbookid='%s'" % (key))
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '操作成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '操作失败','status':'error'}), content_type="application/json");



#根据商品名模糊查询
def goodsNameSelect(request):
    myData = []
    cursor = connection.cursor()
    goodsName = request.POST["goodsName"]
    sqlStr = "SELECT * FROM goods where goodsname like '%%%%%s%%%%'"%(goodsName)

    # 根据商品名精确查询
    if "jingque" in request.POST:
        if request.POST["jingque"] == "true":
            sqlStr = "SELECT * FROM goods where goodsname = '%s'"%(goodsName)

    cursor.execute(sqlStr);
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = {
                'goodsid':row[0],
                'rebate':row[1],
                'lookhistoryid':row[2],
                'standard':row[3],
                'images':row[4],
                'price':row[5],
                'details':row[6],
                'color':row[7],
                'size':row[8],
                'principal':row[9],
                'counts':row[10],
                'stock':row[11],
                'shopname':row[12],
                'status':row[13],
                'uptime':row[14].strftime('%Y-%m-%d %H:%M:%S'),
                'downtime':row[15].strftime('%Y-%m-%d %H:%M:%S'),
                
                'goodsname':row[16],
                
                'transportmoney':row[17],
                'proprice':row[18],
                'prostart':row[19].strftime('%Y-%m-%d'),
                'proend':row[20].strftime('%Y-%m-%d'),
                'addtime':row[21].strftime('%Y-%m-%d %H:%M:%S'),
                'sellcount':row[22],
                'isinfudai':row[23],
                'isinmiaosha':row[24] , 
                'keywords':row[25]
            }
            myData.append(goods);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");




#留言接口
def leavingMessAdd(request):
    data = request.POST
    #测试数据
    # userid = "2017121610132964" 
    # leavemessage = "啊实打实大所大是打算打算啊实打实大所大所大所大所大所，"
    userid = data["userid"];
    leavemessage = data["leavemessage"]
    #根据时间随机生成guestbookid
    guestbookid = randomString()
    cursor=connection.cursor();
    result = cursor.execute("INSERT INTO guestbook(guestbookid , userid , leavemessage)VALUES('%s' , '%s' , '%s')"%(guestbookid , userid , leavemessage))
    cursor.close();
    if result == 1:
        return HttpResponse(json.dumps({'message': '留言成功','status':'ok'}), content_type="application/json");
    else:
        return HttpResponse(json.dumps({'message': '留言失败','status':'error'}), content_type="application/json");

def selectAllleav(data):
    xiaoSB = []
    for ss in data:
        guestbookid = ss[0]
        userid = ss[1]
        leavemessage = ss[2]
        leavtime = str(ss[3])
        status = ss[4]
        username = ss[5]
        ssss = {'guestbookid':guestbookid , 'userid':userid , 'leavemessage':leavemessage , 'leavtime':leavtime , 'status':status , "username":username}
        xiaoSB.append(ssss)
    return(xiaoSB)

#留言页面留言查询接口
def leavingMessageSelectAll(request):
    if request.POST:
        print("-------------0-000000000-------------------");
        data = request.POST
        userName = data.getlist("userid")[0]
        status = data.getlist("status")[0]
        print(userName , status)
        cursor = connection.cursor();
        if userName == "" and status == "0":
            cursor.close();
            return HttpResponse(json.dumps({'message': '请输入内容','status':'error'}), content_type="application/json");
            
        else:
            print("((((((((((((((((((((")
            if status == "0":
                selectCount = 1
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s'"%(userName))
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '用户名不存在','status':'error'}), content_type="application/json");
                    else:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":selectCount}), content_type="application/json");
                        
            elif status == "1":
                if userName == "":
                    cursor.execute("SELECT * from guestbook WHERE status='read'")
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '没有已读留言','status':'ok' , "data":selectCount}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        print("8888888888888888888888");
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":selectCount}), content_type="application/json");
                        
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s' and status='read'"%(userName))
                    selectCount  = cursor.fetchall()
                    if not selectCount:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '用户不存在或没有已读留言','status':'ok' , "data":selectCount}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":selectCount}), content_type="application/json");
                        
            elif status == "2":
                if userName == "":
                    cursor.execute("SELECT * from guestbook WHERE status='unread'")
                    selectCount  = cursor.fetchall();
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '没有未读留言','status':'ok'}), content_type="application/json");
                        
                    else:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":selectCount}), content_type="application/json");
                    
                if userName != "":
                    cursor.execute("SELECT * from guestbook WHERE username='%s' and status='unread'"%(userName))
                    selectCount  = cursor.fetchall()
                    if not selectCount:
                        cursor.close();
                        return HttpResponse(json.dumps({'message': '用户不存在或没有未读留言','status':'ok'}), content_type="application/json");
                    
                    else:
                        cursor.close();
                        selectCount = selectAllleav(selectCount)
                        return HttpResponse(json.dumps({'message': '查询成功','status':'ok' , "data":selectCount}), content_type="application/json");



#购物车删除接口
def cartstableManageJsonOneDelete(request):
    cursor=connection.cursor()
    cartsid = request.GET["id"];

    try:
        result = cursor.execute("DELETE FROM liu_carts WHERE cartsid='%s'" % (cartsid))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")



 
#商品大分类获取接口
def getBigClassify(request):
    myData=[];
    try:
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM bigclassify")
        datas=cursor.fetchall();
        cursor.close()
        for data in datas:
            bigClassifyId=data[0];
            name=data[1];
            tempDic = {"bigClassifyId":bigClassifyId , "name":name}
            myData.append(tempDic)
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"sql语句拼写出错","status":"error"}),content_type="application/json")
    

# 商品大分类添加接口
def addBigClassify(request):
    cursor=connection.cursor()
    bigName = request.POST["bigName"];
    bigclassifyid = randomString()

    try:
        result = cursor.execute("INSERT INTO bigclassify (bigclassifyid , name)VALUES('%s' , '%s')" % (bigclassifyid , bigName) )
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"添加成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"添加失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")


# 商品大分类删除接口
def deleteBigClassify(request):
    cursor=connection.cursor()
    deleteName = request.POST["deleteName"];

    try:
        result = cursor.execute("DELETE FROM bigclassify WHERE name='%s'" % (deleteName))
        if result == 1:
            result = cursor.execute("DELETE FROM minClassify WHERE bigName='%s'" % (deleteName))
            cursor.close()
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
            
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")


 
# 商品小分类获取接口
def getMinClassify(request):
    myData=[];
    try:
        sqlStr = "SELECT * FROM minClassify order by CONVERT(bigName USING gbk) , CONVERT(minName USING gbk)"
        queryValue = ""
        if "queryValue" in request.POST:
            queryValue = request.POST["queryValue"]

        if queryValue != "":
            sqlStr = "SELECT * FROM minClassify where bigName like '%%%%%s%%%%' or minName like '%%%%%s%%%%' order by CONVERT(bigName USING gbk) , CONVERT(minName USING gbk)" % (queryValue , queryValue)
        cursor = connection.cursor();
        cursor.execute(sqlStr)
        datas=cursor.fetchall();
        cursor.close()

        for data in datas:
            minClassifyId=data[1];
            bigName=data[2];
            minName = data[3]
            tempDic = {"minClassifyId":minClassifyId , "bigName":bigName , "minName":minName}
            myData.append(tempDic)
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"sql语句拼写出错","status":"error"}),content_type="application/json")
    

# 商品小分类添加接口
def addMinClassify(request):
    cursor=connection.cursor()
    bigName = request.POST["bigName"];
    minName = request.POST["minName"];
    minClassifyId = randomString()

    try:
        result = cursor.execute("INSERT INTO minClassify (minClassifyId , bigName , minName)VALUES('%s' , '%s' , '%s')" % (minClassifyId , bigName , minName))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"添加成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"添加失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")


# 商品小分类删除接口
def deleteMinClassify(request):
    cursor=connection.cursor()
    deleteBigName = request.POST["deleteBigName"];
    deleteMinName = request.POST["deleteMinName"];

    try:
        result = cursor.execute("DELETE FROM minClassify WHERE bigName='%s' and minName='%s'" % (deleteBigName , deleteMinName))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")




# 推荐商品获取接口
def getRecommendGoods (request):
    myData=[];
    try:
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM recommendGoods")
        datas=cursor.fetchall();
        cursor.close()

        for data in datas:
            recommendId=data[1];
            recommendImg=data[2];
            recommendName = data[3]
            recommendTime = data[4].strftime('%Y-%m-%d %H:%M:%S')
            goodsid = data[5]
            tempDic = {"recommendId":recommendId , "recommendImg":recommendImg , "recommendName":recommendName , "recommendTime":recommendTime , "goodsid":goodsid}
            myData.append(tempDic)
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"商品推荐表查询操作失败","status":"error"}),content_type="application/json")
def testhtml(request):
    return render(request , 'testhtml.html')


# 推荐商品添加接口
def addRecommendGoods (request) :
    names = request.POST.getlist("recommendName")
    goodsIdList = request.POST.getlist("goodsid")
    imgs = request.FILES.getlist("imgsFile")

    try: 
        for itemIndex , item in enumerate(imgs):
            filepath = "./shopApp/static/myfile/recommendGoods";
            imgName = randomString() + ".jpg";
            filename = filepath + "/" + imgName
            
            filename = open(filename , "wb");
            filename.write(item.__dict__["file"].read());
            filename.close();

        
            recommendId = randomString()
            cursor=connection.cursor()
            cursor.execute("INSERT INTO recommendGoods (recommendId , recomendImg , recommendName , goodsid)VALUES('%s' , '%s' , '%s' , '%s')" % (recommendId , "/static/myfile/recommendGoods/" + imgName , names[itemIndex] , goodsIdList[itemIndex]))
            cursor.close()
        statusDic = MyTool.resultOk("插入数据成功")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
            
    
    except Exception as e: 
        statusDic = MyTool.resultError("插入数据失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

  
# 推荐商品删除接口
def delRecommendGoods(request):
    recommendIds = []
    imgs = []

    for key in request.POST:
        if "deleteId" in key:
            recommendIds.append(request.POST[key])
        if "deleteImg" in key:
            imgs.append(request.POST[key])

    cursor=connection.cursor();

    if len(recommendIds) <= 0:
        return HttpResponse(json.dumps({"message":'要删除0个数据吗？' , "status":"error"}) , content_type="application/json");

    try:
        sqlStr = "delete FROM recommendGoods WHERE recommendId in ("
        for deleteId in recommendIds:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        
        deleteCount = cursor.execute(sqlStr);
        cursor.close()

        if deleteCount == len(recommendIds):
            try:
                for imgPath in imgs:
                    imgPath = imgPath.split("/")
                    imgPath = imgPath[len(imgPath) - 1]
                    removePath = "../shopServer/shopApp/static/myfile/" + imgPath
                    os.remove(removePath);
                        
            except Exception as e:
                
                return HttpResponse(json.dumps({'message': '删除图片失败......','status':'ok'}), content_type="application/json");
            
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
     
        
    except Exception as e:
        return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");
