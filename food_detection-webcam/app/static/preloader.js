const prloader = document.querySelector(".preloader")


window.addEventListener("load",()=>{
    setTimeout(() => {
        prloader.classList.add("hide")
    }, 1000);
})