
function getDate(num) {
    //今天时间
    var date1 = new Date();

    var date2 = new Date(date1);
     //num是正数表示之后的时间，num负数表示之前的时间，0表示今天
    date2.setDate(date1.getDate() - num);
   return date2;
}

function setInputDate(e,dt){
    var d = dt == null ? new Date() : dt;
    var day =d.getDate();

     if(d.getMonth()<10){
        var month = "0"+(d.getMonth()+1);
     }

     if(d.getDate()<10){
         day = "0"+d.getDate();
     }

     var datew = d.getFullYear()+"-"+month+"-"+day;
     var datew = datew.toString();
     $(e).val(datew);
}

function getLikeTitleList(){
    getShopList({type:1,likeTitle:$('input[likeTitle]').val()})
}

function getShopByDate(){
    getShopList({type:2,startDate:$('input[type=date]:nth-of-type(1)').val(),endDate:$('input[type=date]:nth-of-type(2)').val()})
}

function getShopList(data){

    if (data == null){
         data = {}
    }
    $.ajax({
        url:'/admin/getMyShops',
        data:data,
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 1){
                $('.list').children().remove();
                if(data.data.length>0){
                    for(var i = 0;i<data.data.length;i++){
                        data.data[i].no=i+1;
                        createShopItem(data.data[i]);
                    }
					initMenu(menuData);
                    notShopData('已经到底了');
                }else{
                    notShopData('没有数据');
                }
            }else{
                if(parent){
                    parent.document.location.href='/'
                }else{
                    document.location.href='/'
                }
            }
        },
        error:function(){}
    });
}

function createShopItem(item){
    var div = $('<div class="item" shopId="'+item.id+'" shopImg="'+item.img+'"></div>');
    div.append('<idv>'+item.no+'</div>');
    div.append('<idv>'+item.title+'</div>');
    div.append('<idv>'+item.price+'</div>');
    div.append('<idv>'+item.number+'</div>');
    div.append('<idv>'+item.payNum+'</div>');
    div.append('<idv>'+item.status+'</div>');
    div.append('<idv>'+item.categoryName+'</div>');
    div.append('<idv>'+item.createTime+'</div>');
    div.append('<idv>右键操作</div>');
    $('.list').append(div);
}

function notShopData(text){
    $('.list').append('<div class="item"><div style="width:99.61%">'+text+'</div></div>');
}

var menuData={
	e:'.item',
	eTitle:true,
	keyCode:3, 
	list:[{name:'修改',click:function(e){
		menuUpdate(getMenuClickItemTarget());
	}},
	{name:'删除',click:function(e){
		updateShopInfo('1',getMenuClickItemTarget());
	}},
	{name:'上架',click:function(e){
		updateShopInfo('2',getMenuClickItemTarget());
	}},
	{name:'下架',click:function(e){
		updateShopInfo('3',getMenuClickItemTarget());
	}},],
	show:function(){},
	hidden:function(){}
};

function menuUpdate(e){
	var html = '<div class="add-box">'+
	                '<form action="#">'+
	                   '<div class="add-bar">'+
	                       '<div class="add-title">修改商品</div>'+
	                       '<img src="../static/images/close_777.png" style="height:12px;" onclick="$(\'.add-box\').remove()"/>'+
	                   '</div>'+
	                   '<div class="ipt-div" style="margin-top:25px;"><span>商品名称：</span><input type="text" class="shop-title" value="'+$(e).children().eq(1).text()+'" placeholder="请输入标题"></div>'+
	                   '<div class="ipt-div"><span>价格：</span><input type="text" class="shop-price" value="'+$(e).children().eq(2).text()+'" placeholder="请输入" onkeyup="checkNum(this)"></div>'+
	                   '<div class="ipt-div"><span>数量：</span><input type="text" class="shop-number" value="'+$(e).children().eq(3).text()+'"></div>'+
	                    '<div class="ipt-div"><span>商品图片：</span><input type="text" class="shop-img" value="'+$(e).attr('shopImg')+'"></div>'+
	                   '<div class="ipt-div" style="display:flex;align-items:top;"><span>商品详情：</span><textarea rows="4" cols="36"></textarea></div>'+
	                   '<div style="margin-top:15px;padding-left:100px;">'+
	                       '<input class="btn-green" style="border:none;border-radius:3px;color:white;margin-right:20px;" type="button" value="修改" onclick="updateBtn()">'+
	                   '</div>'+
	               '</form>'+
	               '<div id="msg"></div>'+
	           '</div>';
	$('body').append(html);
}

function updateBtn(){
    updateShopInfo('4',getMenuClickItemTarget());
}

function updateShopInfo(type,e){
    $.ajax({
        url:'/shop/updateShopStatus',
        data:{
            shopId:$(e).attr('shopId'),
            type:type,
            shopTitle:$('.add-box .shop-title').val(),
            shopPrice:$('.add-box .shop-price').val(),
            number:$('.add-box .shop-number').val(),
            img:$('.add-box .shop-img').val()
         },
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 1){
                $('.add-box').remove();
                getShopList();
            }else if(data.code == -1){
                parent.document.location.href= '/';
            }else{
                $('#msg').text(data.message);
                setTimeout(function(){
                   $('#msg').text('');
                },1500);
            }
        }
    });
}
	
function onLoad(){
	
    setInputDate('input[type=date]:nth-of-type(1)',getDate(7));
    setInputDate('input[type=date]:nth-of-type(2)');
    getShopList();
}