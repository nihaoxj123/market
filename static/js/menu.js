

/*
菜单数据
data={
    e:'.item', //点击那个地方出发菜单
    eTitle:true, //是否点击标题部分失效
    keyCode:3, //1 = 鼠标左键; 2 = 鼠标中键; 3 = 鼠标右键； 4 = 接收前面所有事件
    list:[{name:'购买',click:function(e){}},],
    show:function(){},//e 右击那个item
    hidden:function(){}
};
initMenu(data);
*/

function initHtml(){
	//取消右键
	$('html').on('contextmenu', function (){return false;}).click(function(){
	    hiddenMenu();
	    $('.popup_menu').hide();
	});
}

var menuHiddenCall = null;
var menu_data = null;

//获取触发菜单的目标元素
function getMenuClickItemTarget(){
	if(menu_data){
		return menu_data.clickTarget;
	}
}

//初始化菜单
function initMenu(data){
	menu_data = data;
	initHtml();
    createMenu(data.list);
    menuHiddenCall = data.hidden;
    //显示弹窗
   $(data.e).mousedown(function(e){
         menu_data.clickTarget = e.currentTarget;
        if(data.eTitle && e.currentTarget == $(data.e).eq(0)[0]){
            hiddenMenu();
            return false;
        }
    　　  //e.which 1 = 鼠标左键 left; 2 = 鼠标中键; 3 = 鼠标右键
        if (data.keyCode == 4 || e.which == data.keyCode){
            data.show();
            $('.menu').css({'left':e.clientX+'px','top':e.clientY+'px'}).show();
        }else{
            hiddenMenu();
        }
    　　return false;//阻止链接跳转
   })
}
//创建菜单
function createMenu(list){
    $('.menu').remove();
     var ul = $('<ul class="menu"></ul>');
        for(var i =0;i<list.length;i++){
            menu = list[i];
            var li = $('<li>'+menu.name+'</li>');
            li.click(menu.click);
            ul.append(li);
        }
     $('body').children().eq(0).before(ul);
}

function hiddenMenu(){
    $('.menu').hide();
    if (menuHiddenCall != null){
        menuHiddenCall();
    }
}
