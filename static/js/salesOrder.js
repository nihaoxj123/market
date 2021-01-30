function getOrderList(data){
    if(data == null){
        data = {};
    }

    $.ajax({
        url:'/admin/getPayOrderList',
        data:data,
        type:'post',
        dataType:'json',
        success:function(data){
            if(data.code == 1){
                $('.list').children().remove();
                if(data.data.length>0){
                    for(var i = 0;i<data.data.length;i++){
                        data.data[i].no=i+1;
                        createOrderItem(data.data[i]);
                    }
                    notOrderData('已经到底了');
                }else{
                    notOrderData('没有数据');
                }
            }
        }
    });
}

function createOrderItem(item){
    var div = $('<div class="item" orderId="'+item.id+'" shopId="'+item.shopId+'"></div>');
            div.append('<div>'+item.no+'</div>');
            div.append('<div>'+item.orderId+'</div>');
            div.append('<div>'+item.shopTitle+'</div>');
            div.append('<div>'+item.price+'</div>');
            div.append('<div>'+item.endPrice+'</div>');
            div.append('<div>'+item.orderNumber+'</div>');
            div.append('<div>'+item.createTime+'</div>');
    $('.list').append(div);
}

function notOrderData(text){
    $('.list').append('<div class="item"><div style="width:99.6%">'+text+'</div></div>');
}
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

function onLoad(){
    setInputDate('input[type=date]:nth-of-type(1)',getDate(7));
    setInputDate('input[type=date]:nth-of-type(2)');

    getOrderList();
}
