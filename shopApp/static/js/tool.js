
var HomeUrl = "http://localhost:8000/"

var defaultImageString = "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=317095833,231452967&fm=27&gp=0.jpg"
var defaultMyfilePath = "http://www.dangsh.top/static/myfile/"


function myPost(url, data, fn) {
	var last = url.indexOf("?") == -1 ? "/" : "";
	$.post(HomeUrl + url + last, data,
		function(data) {
			fn(data);
		}
	);

	
}




function myGet(url , successFn , errorFn) {

	$.ajax({
		url: HomeUrl + url + "/",
		success: function (data) {
			successFn(data);
		},
		error: function (msg) {
			errorFn(msg);
		}
	});
}

function myGetParams(url , params , successFn , errorFn) {

	$.ajax({
		url: HomeUrl + url + "/?" + params,
		success: function (data) {
			successFn(data);
		},
		error: function (msg) {
			errorFn(msg);
		}
	});
}



// 订单状态规则
var tool_order_status = ["待审核", "已审核", "待支付", "已支付", "代发货", "已发货", "已取消", "已完成"];

// 创建分页
function createPageNav(selec, totalPages, cbFn) {
	$(selec).twbsPagination({
		totalPages: totalPages,
		first: "首页",
		last: "尾页",
		prev: '上一页',
		next: '下一页',
		startPage: 1,
		visiblePages: totalPages > 5 ? 5 : totalPages , 
		version: '1.1',
		onPageClick: function(event, page) {
			cbFn(event, page)
		}
	});
}

function myPostGoodsManage(url, data, fn) {
	$.ajax({
		url: "http://localhost:8000/" + url + "/",
		type: 'POST',
		data: data,
		traditional: true,
		success: function(data) {
			fn(data);
		}
	});
}


// 商品大分类数据
var bigClassifyData = "";
var isUpdateBigClassifyData = false;
function getBigClassifyData (callBackFn) {
	if (bigClassifyData == ""){
		// 开始获取商品大分类的数据
		myGet("getBigClassify" , function (data) {
			bigClassifyData = data
			callBackFn(bigClassifyData)
		})
	} else {
		// 看看商品大分类数据有没有更新
		// 如果没有直接返回
		if (isUpdateBigClassifyData == false) {
			callBackFn(bigClassifyData)
		} else {
			// 否者重新请求一遍
			myGet("getBigClassify" , function (data) {
				bigClassifyData = data
				isUpdateBigClassifyData = false
				callBackFn(bigClassifyData)
			})
		}
	}
}


// 商品小分类数据
var minClassifyData = "";
var isUpdateMinClassifyData = false;
function getMinClassifyData (callBackFn) {
	if (minClassifyData == ""){
		// 开始获取商品大分类的数据
		myGet("getMinClassify", function (data) {
			minClassifyData = data
			callBackFn(minClassifyData)
		})
	} else {
		// 看看商品大分类数据有没有更新
		// 如果没有直接返回
		if (isUpdateMinClassifyData == false) {
			callBackFn(minClassifyData)
		} else {
			// 否者重新请求一遍
			myGet("getMinClassify" , function (data) {
				minClassifyData = data
				isUpdateMinClassifyData = false
				callBackFn(minClassifyData)
			})
		}
	}
}



// 给时间函数增加扩展势函数
Date.prototype.pattern=function(fmt) {   
	/** * 对Date的扩展，将 Date 转化为指定格式的String * 月(M)、日(d)、12小时(h)、24小时(H)、分(m)、秒(s)、周(E)、季度(q)
    可以用 1-2 个占位符 * 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) * eg: * (new
    Date()).pattern("yyyy-MM-dd hh:mm:ss.S")==> 2006-07-02 08:09:04.423      
 * (new Date()).pattern("yyyy-MM-dd E HH:mm:ss") ==> 2009-03-10 二 20:09:04      
 * (new Date()).pattern("yyyy-MM-dd EE hh:mm:ss") ==> 2009-03-10 周二 08:09:04      
 * (new Date()).pattern("yyyy-MM-dd EEE hh:mm:ss") ==> 2009-03-10 星期二 08:09:04      
 * (new Date()).pattern("yyyy-M-d h:m:s.S") ==> 2006-7-2 8:9:4.18      
 */       
    var o = {         
    "M+" : this.getMonth()+1, //月份         
    "d+" : this.getDate(), //日         
    "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时         
    "H+" : this.getHours(), //小时         
    "m+" : this.getMinutes(), //分         
    "s+" : this.getSeconds(), //秒         
    "q+" : Math.floor((this.getMonth()+3)/3), //季度         
    "S" : this.getMilliseconds() //毫秒         
    };         
    var week = {         
    "0" : "/u65e5",         
    "1" : "/u4e00",         
    "2" : "/u4e8c",         
    "3" : "/u4e09",         
    "4" : "/u56db",         
    "5" : "/u4e94",         
    "6" : "/u516d"        
    };         
    if(/(y+)/.test(fmt)){         
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));         
    }         
    if(/(E+)/.test(fmt)){         
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "/u661f/u671f" : "/u5468") : "")+week[this.getDay()+""]);         
    }         
    for(var k in o){         
        if(new RegExp("("+ k +")").test(fmt)){         
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));         
        }         
    }         
    return fmt;         
}  


// 去除字符串中的空格
function removeStringSpace(str) {
	if (str == null ||str == "" || str.length <= 0) {
		return ""
	}
	return str.replace(/\s/g, "")
}

