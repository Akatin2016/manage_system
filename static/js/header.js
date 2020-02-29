//导航栏标题焦点切换函数
function getFocus($obj) {
    //找到所有增加了focus类样式的元素
    $(".focus").each(function (i, e) {
        //将e转换为JQ对象，删除focus元素（重置）
        $(e).removeClass("focus");
    });
    // 为当前页面的标题添加焦点样式
    $obj.addClass("focus");
};