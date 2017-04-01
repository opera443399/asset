/*
* @desc: base
* @modified: 2017/4/1
* */

$(document).ready(function(){
    $("#search").click(function(){
        $("#form-searching").submit();
    });
    $("#select-language").change(function(){
        $("#form-language").submit();
    });
    $("#checkbox_all").click(function () {
        $("input[name='checkbox_item']").prop('checked', this.checked)
    });
    $("input[name='checkbox_item']").click(function(){
        $("#checkbox_all").prop("checked",$("input[name='checkbox_item']").length == $("input[name='checkbox_item']:checked").length);
    });
});

