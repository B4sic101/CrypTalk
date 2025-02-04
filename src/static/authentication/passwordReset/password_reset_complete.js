$(document).ready(function(){
    const countdown = document.querySelector(".msg p");
    countdownStart(countdown);
});

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function countdownStart(text) {
    for (let i = 3; i > -1; i--){
        text.innerText = `Redirecting to Login Page in ${i}...`;
        await sleep(1000);
    }
    window.location.replace(
        `${window.location.origin}/login/`,
    );
}