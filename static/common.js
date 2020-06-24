window.onload = function () {

    var oTable = document.getElementById("bbsTab");
    var tabletr = document.getElementsByTagName("tr");
    for (var i = 1; i < oTable.rows.length; i++) {
        oTable.rows[i].cells[0].innerHTML = i;
        // if (i % 2 == 0) {
        //     tabletr[i].style.backgroundColor = 'rgba(30, 80, 174,0.3)';
        // }
    };
    setInterval(function () {
        window.location.reload()
    }, 600000)
}