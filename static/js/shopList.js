
function createTime(shop,index,length){
	after = '0';
	last = '0';
	if((index+1) % 5 == 0){
		last = '1';
	}
	if (length % 5 == 0){
		if(length>=5){
			if(index >= length - 5){
				after = '1';
			}
		}
	}else{
		if(index >= (length - length % 5)){
			after = '1';
		}
	}
	
	var html = '<div class="item" after="'+after+'" last="'+last+'">'+
				'<img src="'+shop.img+'">'+
				'<div class="title">'+shop.title+'</div>'+
				'<div><span class="price">￥'+shop.price+'</span></div>'+
				'<div class="shop-sign"><img src="../static/images/dianpu.png"><span>'+shop.shopSign+'</span></div>'+
				'<div class="line"></div>'+
				'<div class="sales"><span>销量</span>&nbsp;<span>'+shop.payNum+'</span></div>'+
			'</div>';
	$('.list').append(html);
}

function getData(){
	$.ajax({
	    url:'/shop/getShopList',
	    data:{},
	    type:'post',
	    dataType:'json',
	    success:function(data){
	        if(data.code == 1){
	            for(var i =0 ;i<data.data.length;i++){
                    createTime(data.data[i],i,data.data.length);
                }
	        }
	    }
	});
}

function onLoad(){

    getData();
}

