/**
 * Created by yang on 2/8/16.
 */
var hght=0;//初始化滚动条总长

var top=0;//初始化滚动条的当前位置

$(document).ready(function(){//DOM的onload事件

    //$(”#mypage”).load(”table.html”);//table.html的内容被加载到mypage元素

    $(window).scroll( function() {//定义滚动条位置改变时触发的事件。

        hght = this.scrollHeight;//得到滚动条总长，赋给hght变量
        console.log("hght");
        top = this.scrollTop;//得到滚动条当前值，赋给top变量

        setInterval("cando();", 2000);//每隔2秒钟调用一次cando函数来判断当前滚动条位置。
    });
    function cando() {

        if (top > parseInt(hght / 3) * 2)//判断滚动条当前位置是否超过总长的2/3，parseInt为取整函数

            show();//如果是，调用show函数加载内容。
    }

    function show(){

        $.get("addition.html", function(data) {//利用jquery的get方法得到table.html内容

            $(".col-lg-9").append(data);//用append方法追加内容到mypage元素。

            hght = 0;//恢复滚动条总长，因为$(”#mypage”).scroll事件一触发，又会得到新值，不恢复的话可能会造成判断错误而再次加载……

            top = 0;//原因同上。
        });
    }
});