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