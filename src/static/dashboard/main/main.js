window.addEventListener("load", () => {
    const chats = document.querySelectorAll(".chatBox");
    const msgTextBox = document.querySelector(".entryField");
    const ACTextBox = document.querySelector(".addContactPopUp .container .input");
    const friendBtn = document.querySelector(".dashboardContainer .sidebar .reflectionProfile .profileConfigs .friendBtn");
    const exitfriendBtn = document.querySelector(".addContactPopUp .exitBtn");
    const submitRequestBtn = document.querySelector(".addContactPopUp .container .submitBtn");

    fixChats();
    chats.forEach((chat) => {
        chat.scrollTop = chat.scrollHeight;
    });

    msgTextBox.addEventListener("keydown", msgKeyPressed);
    friendBtn.addEventListener("click", toggleAddContact);
    ACTextBox.addEventListener("keydown", ACkeyPressed);
    exitfriendBtn.addEventListener("click", toggleAddContact);
    submitRequestBtn.addEventListener("click", addContact);
});

function fixChats(){
    const receiverMessages = document.querySelectorAll(".receiver .contact .message");

    receiverMessages.forEach((message) => {
        const messageProps = message.getBoundingClientRect();
        const originWidth = messageProps.width;
        
        message.style.minWidth = `${originWidth}px`;
        message.parentElement.parentElement.style.marginLeft = `${90}%`;
    });
};

function msgKeyPressed(event){
    const key = event.key;
    if (key == "Enter"){
        event.preventDefault();
        sendMessage();
    };
}

function ACkeyPressed(event){
    const key = event.key;
    if (key == "Enter"){
        event.preventDefault();
        addContact();
    };
}

function toggleAddContact(){
    const popup = document.querySelector(".addContactPopUp")
    if (popup.style.display == "block"){
        popup.style.display = "none";
    }
    else{
        popup.style.display = "block";    
    }
}

debug = false
function addContact(){
    if (!debug){
        debug = true;
        const userToAdd = document.querySelector(".addContactPopUp .container .input");
        const msg = document.querySelector(".addContactPopUp .container .msg");

        console.log(`We are going to add ${userToAdd.value}`);

        userToAdd.value = "";
        debug = false;
    }
}

function sendMessage(){
    // Send message here
};

/* CONDITIIONS TO SEND AN INPUT FROM ENTRY FIELD:
    - Is a current contact selected?
    - Is current contact selected valid?
*/