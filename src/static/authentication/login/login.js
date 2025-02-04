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
    $(".fa-regular").click(function(){
        if (!isToggled){
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