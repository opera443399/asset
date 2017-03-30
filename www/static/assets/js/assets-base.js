/* base */
$(document).ready(function(){
    $("#search").click(function(){
        $("#form-searching").submit();
    });
    $("#select-language").change(function(){
        $("#form-language").submit();
    });
});
