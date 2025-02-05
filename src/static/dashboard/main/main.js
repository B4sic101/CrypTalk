const frSocket = new WebSocket(`ws://${window.location.host}/ws/notifyFR/`);
let csrftoken;

window.addEventListener("load", () => {
    const chats = document.querySelectorAll(".chatBox");
    const FRs = document.querySelectorAll(".contacts .friendRequest");
    const msgTextBox = document.querySelector(".entryField");
    const ACTextBox = document.querySelector(".addContactPopUp .container .input");
    const friendBtn = document.querySelector(".dashboardContainer .sidebar .reflectionProfile .profileConfigs .friendBtn");
    const exitfriendBtn = document.querySelector(".addContactPopUp .exitBtn");
    const submitRequestBtn = document.querySelector(".addContactPopUp .container .submitBtn");
    csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    fixChats();
    chats.forEach((chat) => {
        chat.scrollTop = chat.scrollHeight;
    });

    FRs.forEach((fr) => {
        const acceptBtn = fr.querySelector(".acceptBtn");
        const rejectBtn = fr.querySelector(".rejectBtn");
        
        acceptBtn.addEventListener("click", acceptFR);
        rejectBtn.addEventListener("click", rejectFR);
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

                             
                            if (statusCode === 404 || statusCode === 400){
                                msg.innerText = infoMsg;
                                msg.style.color = "rgb(205, 50, 50)";
                                foundResponse = true;
                            } else if (statusCode === 201 && !foundResponse) {
                                msg.style.color = "rgb(68, 205, 50)";
                                msg.innerText = infoMsg;
                                foundResponse = true;
                                
                                frSocket.send(JSON.stringify({requestID:reqID}));

                            } else if (!foundResponse) {
                                msg.innerText = "Something went wrong.";
                                msg.style.color = "rgb(205, 50, 50)";
                            };
                            
                        });
                });
             
            userToAdd.value = "";
            debug = false;
        };
    };
}

frSocket.onmessage = function(event) {
    displayFR(event);
}

function displayFR(event){
    const requestDetails = JSON.parse(event.data);
    const contactList = document.querySelector(".contacts");
    const template = document.querySelector(".FRTemplate");

    const tempDup = template.cloneNode(true);
    const FRDiv = tempDup.content.querySelector(".friendRequest");

    const requestID = FRDiv.querySelector(".friendRequestID");
    requestID.innerText = requestDetails.requestID;

    const sender = FRDiv.querySelector(".contactUsername");
    sender.innerText = requestDetails.sender;

    const senderID = requestDetails.senderID;

    const profile = FRDiv.querySelector("img");
    profile.src = `/uploads/profiles/user_${senderID}.jpeg`

    contactList.appendChild(FRDiv);
    
    const acceptBtn = FRDiv.querySelector(".acceptBtn");
    const rejectBtn = FRDiv.querySelector(".rejectBtn");

    acceptBtn.addEventListener("click", acceptFR);
    rejectBtn.addEventListener("click", rejectFR);
}

function rejectFR(){
    // Rejecting Friend Requests
    console.log(this.classList[1]);
    const frDiv = document.querySelector(`.${this.classList[1]}`).parentElement;
    const reqID = this.classList[1];
    fetch(`/api/rejectFR?requestID=${reqID}`)
        .then(data => {
            return data.status;
        })
        .then(statusCode => {
            // If the friend request was deleted succesfully, reflect the changes
            if (statusCode == 200){
                frDiv.remove()
            }
        })
}

function acceptFR(){
    // Accepting Friend Requests
    let statusCode;
    const reqID = this.querySelector(".friendRequestID").innerText;
    const frDiv = document.querySelector(`.${reqID}`)
    fetch(`/api/acceptFR?reqid=${reqID}`)
        .then(data => {
            statusCode = data.status;
            return data.json();
        })
        .then(response => {
            // If chat created, reflect changes
            if (statusCode == 201){
                frDiv.remove()
            }
        })
}

function sendMessage(){
    // Send message here
};

/* CONDITIIONS TO SEND AN INPUT FROM ENTRY FIELD:
    - Is a current contact selected?
    - Is current contact selected valid?
*/