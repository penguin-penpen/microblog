/**
 * Created by yang on 2/8/16.
 */

$(document).ready(function(){//DOM的onload事件
    $(window).scroll( function() {//定义滚动条位置改变时触发的事件。
        //回到顶部按钮
        if (getScrollTop() > 1000) {//当滚动条离开顶端时，显示"回到顶部"。这里写20的原因是，"回到顶端"按钮也不是需要马上出现，根据自己的需求 而设置。
            //$("#top_div").show();
            //alert("left");
            $("#back-to-top").show();
        }
        else {//当滚动条回到顶端时，将"回到顶端按钮"  隐藏
            $("#back-to-top").hide();
            //     alert("back");
        }
        //点击返回顶部
        var clickState = 0;
        $("#back-to-top").click(function() {
            $(document.body).animate({scrollTop: 0}, 800);
            return false;
            //clickState = 0;
            //$(document).animate({scrollTop:0}, 500);
            //$(document).scrollTop(0);
            //if(clickState == 0){
            //    $('html, body').animate({scrollTop:0}, 500);
            //    clickState = 1;
            //}
        });

        //主页滑动加载更多
        if(document.title == 'Home - Penguin\'s blog'){
            var len = $(document).height();
            if (getScrollTop() > 0.7 * len){
                //alert("show!");
                load("index-addition", ".col-lg-9");
            }
        }
    });


});
//获取滚动条的位置
function getScrollTop() {
    var scrollPos;
    if (window.pageYOffset)
    {
        scrollPos = window.pageYOffset;
    }
    else if (document.compatMode && document.compatMode != 'BackCompat')
    {
        scrollPos = document.documentElement.scrollTop;
    }
    else if (document.body)
    {
        scrollPos = document.body.scrollTop;
    }
    return scrollPos;
}
/*
 * load()加载更多内容
 * url：加载的页面
 * position：加载内容所放的元素
 */
function load(url, position){
    //alert("show");
    $.get(url, function(data) {//function为回调函数，把请求url后得到的结果作为data参数

        $(position).append(data);//用append方法追加内容到mypage元素。

        //hght = 0;//恢复滚动条总长，因为$(”#mypage”).scroll事件一触发，又会得到新值，不恢复的话可能会造成判断错误而再次加载……
        //top = 0;//原因同上。
    });
}
//跨浏览器获取滚动条位置，sp == scroll position
function getSP(){
    top = document.documentElement.scrollTop || document.body.scrollTop;

    return top;
    //left : document.documentElement.scrollLeft || document.body.scrollLeft;

}
