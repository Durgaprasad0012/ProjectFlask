$(function(){
    $(".bookmark").hide()
    $("#about").click(function(){
        $(".content-section").fadeIn(3000);
        setTimeout(() => {
            $(".content-section").fadeOut(3000);
        }, 10000);
    })
    $("#mb").mouseover(function(){
        $(".bookmark").hide()
    })
    $("#sb").mouseover(function(){
        $(".bookmark").show()
    })
})