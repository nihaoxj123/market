
var categoryList = [];

function checkNum(obj) {
    obj.value = obj.value.replace(/^0*/g, '');//第一个数不能为0 ，若为0替换为空
    obj.value = obj.value.replace(/[^\d.]/g, "");//是否是数字 和小数点，若是除数字 和小数点之外的则替换为空
    obj.value = obj.value.replace(/^\./g, "");//确证第一个为数字而不是“.”
    obj.value = obj.value.replace(/\.{2,}/g, ".");//只能输入一个“.”
    obj.value = obj.value.replace(".", "$#$").replace(/\./g, "").replace("$#$", ".");//保证”.“只出现一次，而不能出现两次以上
    obj.value = obj.value.replace(/^(\-)*(\d+)\.(\d\d).*$/, '$1$2.$3');//只能输入两个小数
}

function addBtnClick(){
    if (categoryList != null && categoryList.length > 0){
        showAddShopBox();
    }else{
        getData();
    }

}

function getData(){
    $.ajax({
        url:'/admin/getCategoryList',
        data:{},
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 1){
                categoryList = data.data;
                showAddShopBox();
            }
        }
    });
}
function addShop(){

    $.ajax({
        url:'/shop/addShop',
        data:{
            shopTitle:$('.shop-title').val(),
            shopPrice:$('.shop-price').val(),
            number:$('.shop-number').val(),
            shopImg:$('.shop-img').val(),
            cId:$('.ipt-div select').val()
            },
        type:'post',
        dataType:'json',
        success:function(data){

            if(data.code == 1){
                document.location.href='/admin/salesShopPage'
            }else if(data.code == -1){
                parent.document.location.href='/'
            }else{
                $('#msg').text(data.message);
                setTimeout(function(){
                    $('#msg').text('');
                },1500);
            }
        }
    });

}
function showAddShopBox(){
    options = '';
    for(var i =0;i<categoryList.length;i++){
        options += '<option value="'+categoryList[i].id+'">'+categoryList[i].name+'</option>';
    }
    var html = '<div class="add-box">'+
                    '<form action="#">'+
                       '<div class="add-bar">'+
                           '<div class="add-title">添加商品</div>'+
                           '<img src="../static/images/close_777.png" style="height:12px;" onclick="$(\'.add-box\').remove()"/>'+
                       '</div>'+
                       '<div class="ipt-div" style="margin-top:25px;"><span>商品名称：</span><input type="text" class="shop-title" placeholder="请输入标题"></div>'+
                       '<div class="ipt-div"><span>价格：</span><input type="text" class="shop-price" placeholder="请输入" onkeyup="checkNum(this)"></div>'+
                       '<div class="ipt-div"><span>数量：</span><input type="number" class="shop-number" value="0"></div>'+
                       '<div class="ipt-div">'+
                           '<span>类别：</span>'+
                           '<select value="'+categoryList[0].id+'">'+
                                options+
                           '</select>'+
                       '</div>'+
                       '<div class="ipt-div"><span>商品图片：</span><input type="text" class="shop-img"></div>'+
                       '<div class="ipt-div" style="display:flex;align-items:top;"><span>商品详情：</span><textarea rows="4" cols="36"></textarea></div>'+
                       '<div style="margin-top:15px;padding-left:100px;">'+
                           '<input class="btn-green" style="border:none;border-radius:3px;color:white;margin-right:20px;" type="button" value="添加" onclick="addShop()">'+
                           '<input class="btn-green" style="border:1px solid #ddd;background-color:white;color:#666;" type="reset" value="重置">'+
                       '</div>'+
                   '</form>'+
                   '<div id="msg"></div>'+
               '</div>';
    $('body').append(html);
}