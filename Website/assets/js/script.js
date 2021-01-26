console.log(window.scrollY)

function header_reset(){
    document.getElementById("add").style.borderWidth = "0px"
    document.getElementById("capabilities").style.borderWidth = "0px"
    document.getElementById("help").style.borderWidth = "0px"
}

window.onscroll = () => {
    console.log(window.scrollY)

    if (window.scrollY >= 0 && window.scrollY < 400){
        header_reset()
        document.getElementById("add").style.borderWidth = 'medium';
    } else if (window.scrollY > 400 && window.scrollY < 900){
        header_reset()
        document.getElementById("capabilities").style.borderWidth = 'medium';
    } else if (window.scrollY > 900){
        header_reset()
        document.getElementById("help").style.borderWidth = 'medium';
    }
}

var scapabilities = document.getElementById("scroll_capabilities");
var sadd = document.getElementById("scroll_add");
var shelp = document.getElementById("scroll_help");

var capabilities = document.getElementById("capabilities");
var add = document.getElementById("add");
var help = document.getElementById("help");
capabilities.onclick = function(){
    scapabilities.scrollIntoView({block: "center", behavior: "smooth"});
}

add.onclick = function(){
    sadd.scrollIntoView({block: "center", behavior: "smooth"});
}

help.onclick = function(){
    shelp.scrollIntoView({block: "center", behavior: "smooth"});
}