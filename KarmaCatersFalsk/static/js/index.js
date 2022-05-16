$(function(){
    $(".content").mouseover(function(){
        $('#book').fadeIn(2000);
    })
    $("#about").click(function(){
        $(".content-section").fadeIn(3000);
        setTimeout(() => {
            $(".content-section").fadeOut(3000);
        }, 10000);
    })
})