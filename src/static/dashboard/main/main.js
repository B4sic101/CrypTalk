const frSocket = new WebSocket(`ws://${window.location.host}/ws/notifyFR/`);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`);
let csrftoken;

window.addEventListener("load", () => {
    const chats = document.querySelectorAll(".chatBox");
    const FRs = document.querySelectorAll(".contacts .friendRequest");
    const msgBoxes = document.querySelectorAll(".msgBox");
    const contacts = document.querySelectorAll(".contact");
    const ACTextBox = document.querySelector(".addContactPopUp .container .FRInput");
    const friendBtn = document.querySelector(".dashboardContainer .sidebar .reflectionProfile .profileConfigs .friendBtn");
    const exitfriendBtn = document.querySelector(".addContactPopUp .exitBtn");
    const submitRequestBtn = document.querySelector(".addContactPopUp .container .submitBtn");
    csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    chats.forEach((chat) => {
        chat.scrollTop = chat.scrollHeight;
    });
    msgBoxes.forEach((msgBox) => {
        const inputField = msgBox.querySelector(".typeBox")
        inputField.addEventListener("keydown", msgKeyPressed);
    });

    FRs.forEach((fr) => {
        const acceptBtn = fr.querySelector(".acceptBtn");
        const rejectBtn = fr.querySelector(".rejectBtn");
        
        acceptBtn.addEventListener("click", acceptFR);
        rejectBtn.addEventListener("click", rejectFR);
    });

    contacts.forEach((contact) => {
        if (!contact.classList.contains("friendRequest") && !contact.classList.contains("profileOfContact")){
            contact.addEventListener("click", chatSelected);
        }
    });

    //fixChats();

    friendBtn.addEventListener("click", toggleAddContact);
    ACTextBox.addEventListener("keydown", ACkeyPressed);
    exitfriendBtn.addEventListener("click", toggleAddContact);
    submitRequestBtn.addEventListener("click", addContact);
});

function fixChats(){
    const receiverMessages = document.querySelectorAll(".receiver");

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
    const popup = document.querySelector(".addContactPopUp");
    const msg = document.querySelector(".addContactPopUp .container .msg");
    const inputField = popup.querySelector(".container .FRInput");
    if (popup.style.display == "block"){
        popup.style.display = "none";
        msg.style.display = "none";
        msg.innerText = "";
        inputField.value = "";
    }
    else{
        popup.style.display = "block";    
    }
}

let debug = false
function addContact(){
    if (!debug){
        const userToAdd = document.querySelector(".addContactPopUp .container .FRInput");
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
                                
                                frSocket.send(JSON.stringify({requestID:reqID, type:"sendFR"}));

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
    const requestData = JSON.parse(event.data);
    if (requestData.type == "fr.notifier"){
        displayFR(requestData);
    }
}

chatSocket.onmessage = function(event) {
    const requestData = JSON.parse(event.data);
    if (requestData.type == "chat.create"){ 
        createChat(requestData);
    }
}

function displayFR(requestData){
    const contactList = document.querySelector(".contacts");
    const template = document.querySelector(".FRTemplate");

    const tempDup = template.cloneNode(true);
    const FRDiv = tempDup.content.querySelector(".friendRequest");

    const requestIDs = FRDiv.querySelectorAll(".requestID");
    requestIDs.forEach((request) => {
        request.innerText = requestData.requestID;
    })

    const sender = FRDiv.querySelector(".contactUsername");
    sender.innerText = requestData.sender;

    const senderID = requestData.senderID;

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
    const reqIDiv = this.querySelector(".requestID");
    const frDiv = reqIDiv.parentElement.parentElement;
    const reqID = reqIDiv.innerText;

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
    const reqIDiv = this.querySelector(".requestID");
    const frDiv = reqIDiv.parentElement.parentElement;
    const reqID = reqIDiv.innerText;

    let statusCode;
    fetch(`/api/acceptFR?requestID=${reqID}`)
        .then(data => {
            statusCode = data.status;
            return data.json();
        })
        .then(response => {
            // If chat created, reflect changes
            if (statusCode == 201){
                frDiv.remove();
                console.log(`Encryption Key = ${response.cryptKey}`);
                console.log(`iv = ${response.iv}`);
                // Send message to websocket to display to other user
                createChat(response);
                chatSocket.send(JSON.stringify({chatID:response.chatID, type:"createChat"}));
            }
        })
}

function createChat(chatData){
    // Create a client side chat
    // Latest Message stays hidden till decrypted
    const contactList = document.querySelector(".contacts");
    const template = document.querySelector(".contactTemplate");

    const tempDup = template.cloneNode(true);
    const contactDIV = tempDup.content.querySelector(".contact");

    let chatID = contactDIV.querySelector(".chatID");
    chatID.innerText = chatData.chatID;

    let sender = contactDIV.querySelector(".contactUsername");
    sender.innerText = chatData.username;

    const senderID = chatData.sender;

    let profile = contactDIV.querySelector("img");
    profile.src = `/uploads/profiles/user_${senderID}.jpeg`

    contactList.appendChild(contactDIV);

    const msgBoxTemp = document.querySelector(".msgBoxTemplate");

    const msgBoxTempDup = msgBoxTemp.cloneNode(true);
    const msgBox = msgBoxTempDup.content.querySelector(".msgBox");

    chatID = msgBox.querySelector(".details .chatID")
    chatID.innerText = chatData.chatID;

    sender = msgBox.querySelector(".msgTopBar .contact .contactUsername");
    sender.innerText = chatData.username;

    profile = msgBox.querySelector(".msgTopBar .contact img");
    profile.src = `/uploads/profiles/user_${senderID}.jpeg`

    const cryptKey = msgBox.querySelector(".details .cryptKey");
    cryptKey.innerText = chatData.cryptKey;
    
    const iv = msgBox.querySelector(".details .iv");
    iv.innerText = chatData.iv;

    const dashboardContainer = document.querySelector(".dashboardContainer");

    dashboardContainer.appendChild(msgBox);
    // add event listeners to the MsgBox divs

    contactDIV.addEventListener("click", chatSelected);
    
}

let selectedChat = "";

function chatSelected(){
    const chatID = this.querySelector(".chatID").innerText;
    const dashboardContainer = document.querySelector(".dashboardContainer");
    const dummyMsgBox = document.querySelector(".dummyMsgBox");
    const welcomeMsg = document.querySelector(".welcomeMsg");

    if (selectedChat == ""){

        const msgBoxes = document.querySelectorAll(".dashboardContainer .msgBox");
        let contactsMsgBox;

        msgBoxes.forEach((msgBox) => {
            const boxChatID = msgBox.querySelector(".details .chatID").innerText;
            if (chatID == boxChatID){
                contactsMsgBox = msgBox;
            }
        });
        
        dashboardContainer.appendChild(contactsMsgBox);
        contactsMsgBox.style.display = "block";

        dummyMsgBox.style.display = "none";
        welcomeMsg.style.display = "none";

        selectedChat = chatID;
        this.classList.add("active");
        // Add .selected class to the contact and display the relevant chat
    } else if (selectedChat == chatID){
        // Hide the msg box and remove selected class off of it

        const msgBoxes = document.querySelectorAll(".dashboardContainer .msgBox");
        let contactsMsgBox;

        msgBoxes.forEach((msgBox) => {
            const boxChatID = msgBox.querySelector(".details .chatID").innerText;
            if (chatID == boxChatID){
                contactsMsgBox = msgBox;
            }
        });

        contactsMsgBox.style.display = "none";
        this.classList.remove("active");

        dummyMsgBox.style.display = "block";
        welcomeMsg.style.display = "block";

        selectedChat = "";
    }
    //WHAT HAPPENS WHEN THERE IS A CHAT SELECTED?
    /* Do this when selected

    const dummyMsgBox = document.querySelector(".dummyMsgBox");
    dummyMsgBox.style.display = 'none'
    */
    // Remove .active class on any other chat and hide their 
}

function sendMessage(){
    // Send message here
};

/* CONDITIIONS TO SEND AN INPUT FROM ENTRY FIELD:
    - Is a current contact selected?
    - Is current contact selected valid?
*/