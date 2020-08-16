window.onload = function (){
    var oTable = document.getElementById("bbsTab");
    var tabletr = document.getElementsByTagName("tr");
    for (var i = 1; i < oTable.rows.length; i++) {
        oTable.rows[i].cells[0].innerHTML = i;
        if (i % 2 == 0) {
            tabletr[i].style.backgroundColor = 'rgba(200, 189, 136,.4)';
        }
    };
    setInterval(function () {
        window.location.reload()
    }, 1800000);
    var tel=document.getElementById("tel");
    
    var reg = /^(\d{3})\d{4}(\d{4})$/g;  
    tel.replace(reg, "$1****$2");
    
}