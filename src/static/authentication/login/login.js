window.addEventListener("load", () => {
    let isToggled = false;

});

let isToggled = false;
$(document).ready(function(){
    const passwdToggle = document.querySelector(".fa-eye");
    const passwordField = document.querySelector(".passwordInput");
    console.log(`Toggle height: ${passwdToggle.style.height}, Field height: ${passwordField.style.height}`)
    passwdToggle.style.height = `${passwordField.style.height}px`;
    $(".fa-regular").click(function(){
        if (isToggled){
            hidePasswd(this);
        }
        else {
            showPasswd(this);
        }
        isToggled = !isToggled;
    });
});

function showPasswd(passwdToggle){
    passwdToggle.classList.replace("fa-eye", "fa-eye-slash");
    const passwdInput = document.querySelector(".passwordInput");
    passwdInput.type = "text";
};

function hidePasswd(passwdToggle){
    passwdToggle.classList.replace("fa-eye-slash", "fa-eye");
    const passwdInput = document.querySelector(".passwordInput");
    passwdInput.type = "password";
};