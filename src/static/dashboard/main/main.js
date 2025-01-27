const frSocket = new WebSocket(`ws://${window.location.host}/ws/notifyFR/`);

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
    const msg = document.querySelector(".addContactPopUp .container .msg");
    if (popup.style.display == "block"){
        popup.style.display = "none";
        msg.style.display = "none";
        msg.innerText = "";
    }
    else{
        popup.style.display = "block";    
    }
}

let debug = false
function addContact(){
    if (!debug){
        const userToAdd = document.querySelector(".addContactPopUp .container .input");
        if (userToAdd != ""){
            debug = true;
            const msg = document.querySelector(".addContactPopUp .container .msg");
            let userid;
            let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            let statusCode = 0;
            fetch(`/api/get-userid?username=${userToAdd.value}`)
                .then(data => {return data.json();})
                .then(post => {
                    userid = post.userID;
                    fetch("/api/add-contact", {
                        method: "POST",
                        headers: {'Content-Type':'application/json', 'X-CSRFToken':csrftoken},
                        body: JSON.stringify({receiver:userid})
                    })
                        .then(data => {
                            statusCode = data.status;
                            return data.json();
                        })
                        .then(response => {
                            msg.style.display = "block";
                            let foundResponse = false;
                            let infoMsg = response.msg
                            let reqID = response.requestID
                            console.log("Check 1")

                            
                            if (statusCode === 404 || statusCode === 400){
                                msg.innerText = infoMsg;
                                msg.style.color = "rgb(205, 50, 50)";
                                foundResponse = true;
                            } else if (statusCode === 201 && !foundResponse) {
                                msg.style.color = "rgb(68, 205, 50)";
                                msg.innerText = infoMsg;
                                foundResponse = true;
                                console.log("Check 2")
                                frSocket.onopen = (event) => {
                                    console.log("Check 3")
                                    frSocket.send({'requestID': reqID});
                                    console.log("Websocket Message sent")
                                };
                            } else if (!foundResponse) {
                                msg.innerText = "Something went wrong.";
                                msg.style.color = "rgb(205, 50, 50)";
                            };
                            console.log("Check 4")
                        });
                });
             
            userToAdd.value = "";
            debug = false;
        };
    };
}

frSocket.onmessage = function(event) {
    const reqID =  event.requestID;
    const senderUsername = event.senderUsername;
    addFR(reqID, senderUsername);
}

function addFR(request, username){
    const contactList = document.querySelector(".contacts");
    const template = document.querySelector(".FRTemplate");

    const FRDiv = template.cloneNode(true);
    const requestBody = FRDiv.querySelector(".friendRequest");
    // Make an API to fetch necessary FRDetails

    newFRDiv.appendChild(contactList);
}

function sendMessage(){
    // Send message here
};

/* CONDITIIONS TO SEND AN INPUT FROM ENTRY FIELD:
    - Is a current contact selected?
    - Is current contact selected valid?
*/