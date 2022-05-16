const profile = document.querySelector('.navbar-brand');
const menu = document.querySelector('.profile');
const content = document.querySelector('.content');


profile.onclick = () =>{
    menu.style.visibility = "visible";
}
setTimeout(() => {
    menu.style.visibility = "hidden";
}, 10000);