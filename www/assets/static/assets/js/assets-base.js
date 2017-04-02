/*
* @desc: base
* @modified: 2017/4/2
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

    $("#select-bizunit").change(function(){
        var checked_item_ids=[];
        $('input[name="checkbox_item"]:checked').each(function(){
            checked_item_ids.push($(this).val());
        });
        var checked_item_ids_str=checked_item_ids.join('-');
        $('input[name="checked_item_ids_bizunit"]').val(checked_item_ids_str);
        $("#form-bizunit").submit();
    });

    $("#select-runenv").change(function(){
        var checked_item_ids=[];
        $('input[name="checkbox_item"]:checked').each(function(){
            checked_item_ids.push($(this).val());
        });
        var checked_item_ids_str=checked_item_ids.join('-');
        $('input[name="checked_item_ids_runenv"]').val(checked_item_ids_str);
        $("#form-runenv").submit();
    });
});

