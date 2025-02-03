window.addEventListener("load", () => {
    const passwdToggle = document.querySelector(".fa-eye");
    let isToggled = false;
    passwdToggle.addEventListener("click", function(event){
        if (!isToggled){
            showPasswd(passwdToggle);
            isToggled = true;
        }
        else {
            hidePasswd(passwdToggle);
            isToggled = false;
        }
    });
});

let isToggled = false;
$(document).ready(function(){
    $(".passwordInput .fa-eye").click(function(){
        if (!isToggled){
            showPasswd(this);
        }
        else {
            hidePasswd(this);
        }
    });
});

function showPasswd(passwdToggle){
    passwdToggle.classList.replace("fa-eye", "fa-eye-slash");
    const passwdInput = document.querySelector(".passwordInput");
    passwdInput.type = "text"
};

function hidePasswd(passwdToggle){
    passwdToggle.classList.replace("fa-eye-slash", "fa-eye");
    const passwdInput = document.querySelector(".passwordInput");
    passwdInput.type = "password"
};