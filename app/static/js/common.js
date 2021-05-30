$(document).ready(function () {
    var today = new Date();//定义日期对象     
    var yyyy = today.getFullYear();//通过日期对象的getFullYear()方法返回年      
    var MM = today.getMonth() + 1;//通过日期对象的getMonth()方法返回年      
    var dd = today.getDate();//通过日期对象的getDate()方法返回年  
    var day; //用于保存星期（getDay()方法得到星期编号）  
    if (today.getDay() == 0) day = "星期日 "
    if (today.getDay() == 1) day = "星期一 "
    if (today.getDay() == 2) day = "星期二 "
    if (today.getDay() == 3) day = "星期三 "
    if (today.getDay() == 4) day = "星期四 "
    if (today.getDay() == 5) day = "星期五 "
    if (today.getDay() == 6) day = "星期六 "
    document.getElementById('nowDateTimeSpan').innerHTML = yyyy + "年" + MM + "月" + dd + "日" + " " + day;
    //获得当前<ul>
    var $uList = $(".scroll-box ul");
    var timer = null;
    //触摸清空定时器
    $uList.hover(function () {
        clearInterval(timer);
    }, function () { //离开启动定时器
        timer = setInterval(function () {
            scrollList($uList);
        },
            3000);
    }).trigger("mouseleave"); //自动触发触摸事件
    //滚动动画
    function scrollList(obj) {
        //获得当前<li>的高度
        var scrollHeight = $("ul li:first").height();
        //滚动出一个<li>的高度
        $uList.stop().animate({
            marginTop: -scrollHeight
        }, 600, function () {
            //动画结束后，将当前<ul>marginTop置为初始值0状态，再将第一个<li>拼接到末尾。
            $uList.css({
                marginTop: 0
            }).find("li:first").appendTo($uList);
        });
    }
    
})