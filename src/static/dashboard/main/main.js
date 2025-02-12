const frSocket = new WebSocket(`ws://${window.location.host}/ws/notifyFR/`);
const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/`);
var activeChats = {};
let csrftoken;

window.addEventListener("load", () => {
    const chats = document.querySelectorAll(".chatBox");
    const FRs = document.querySelectorAll(".contacts .friendRequest");
    const contacts = document.querySelectorAll(".contact");
    const ACTextBox = document.querySelector(".addContactPopUp .container .FRInput");
    const friendBtn = document.querySelector(".dashboardContainer .sidebar .reflectionProfile .profileConfigs .friendBtn");
    const exitfriendBtn = document.querySelector(".addContactPopUp .exitBtn");
    const submitRequestBtn = document.querySelector(".addContactPopUp .container .submitBtn");
    csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    chats.forEach((chat) => {
        chat.scrollTop = chat.scrollHeight;
    });

    FRs.forEach((fr) => {
        const acceptBtn = fr.querySelector(".acceptBtn");
        const rejectBtn = fr.querySelector(".rejectBtn");
        
        acceptBtn.addEventListener("click", acceptFR);
        rejectBtn.addEventListener("click", rejectFR);
    });

    contacts.forEach((contact) => {
        if (contact.parentElement.classList.contains("contacts") && !contact.classList.contains("friendRequest")){
            
            const chatID = contact.querySelector(".chatID").innerText;
            if (activeChats[chatID] == undefined){
                let statusCode;
                    fetch(`/api/getChatDetails?chatID=${chatID}`)
                        .then(data => {
                            statusCode = data.status;
                            return data.json()})
                        .then(post => {
                            if (statusCode == 200){
                                newChat = new Chat(post, "createChat");
                                activeChats[post.chatID] = newChat;
                            }
                        })
            }
        }
    });

    friendBtn.addEventListener("click", toggleAddContact);
    ACTextBox.addEventListener("keydown", ACkeyPressed);
    exitfriendBtn.addEventListener("click", toggleAddContact);
    submitRequestBtn.addEventListener("click", addContact);
});

function msgKeyPressed(event){
    const key = event.key;
    if (key == "Enter"){
        event.preventDefault();
        const msgBox = this.parentElement
        const chatID = msgBox.querySelector(".details .chatID").innerText;
        const chatObj = activeChats[chatID];
        if (chatObj !== undefined){
            chatObj.sendMessage(this, msgBox);
        }
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
        if (activeChats[requestData.chatID] == undefined){
            newChat = new Chat(requestData, "fr");
            activeChats[requestData.chatID] = newChat;
        }
    }
    if (requestData.type == "chat.send.message"){
        const chatObj = activeChats[requestData.chatID];
        if (chatObj !== undefined){
            chatObj.receivedMessage(requestData);
        }
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
            if (statusCode == 201){
                frDiv.remove();

                const newChat = new Chat(response, "fr");
                activeChats[response.chatID] = newChat;

                chatSocket.send(JSON.stringify({chatID:response.chatID, type:"createChat"}));
            }
        })
}

class Chat{
    #_contactDIV;
    #_chatID;
    #_username;
    #_cryptKey;
    #_iv;
    #_msgBox;
    constructor(chatData, type){
        if (type == "fr"){
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
            this.#_contactDIV = contactDIV;
        }

        const senderID = chatData.sender;
        const msgBoxTemp = document.querySelector(".msgBoxTemplate");
        
        const msgBoxTempDup = msgBoxTemp.cloneNode(true);
        const msgBox = msgBoxTempDup.content.querySelector(".msgBox");
    
        const chatID = msgBox.querySelector(".details .chatID")
        chatID.innerText = chatData.chatID;
    
        const sender = msgBox.querySelector(".msgTopBar .contact .contactUsername");
        sender.innerText = chatData.username;
    
        const profile = msgBox.querySelector(".msgTopBar .contact img");
        profile.src = `/uploads/profiles/user_${senderID}.jpeg`

        if (this.contactDIV == undefined){
            const contacts = document.querySelectorAll(".contact");
        
            contacts.forEach((contact) => {
                if (contact.parentElement.classList.contains("contacts") && !contact.classList.contains("friendRequest")){
                    if (contact.querySelector(".chatID").innerText == chatData.chatID){
                        this.#_contactDIV = contact;
                    }
                }
            })
        }


        this.#_chatID = chatData.chatID;
        this.#_username = chatData.username;
        this.#_cryptKey = chatData.cryptKey;
        this.#_iv = chatData.iv;
        this.#_msgBox = msgBox;
    
        const dashboardContainer = document.querySelector(".dashboardContainer");
    
        dashboardContainer.appendChild(msgBox);
    
        this.#_contactDIV.addEventListener("click", chatSelected);
        
        const msgBoxes = document.querySelectorAll(".dashboardContainer .msgBox");
        msgBoxes.forEach((msgBox) => {
            if (!msgBox.classList.contains("dummyMsgBox")){
                const inputField = msgBox.querySelector(".entryField");
                inputField.addEventListener("keydown", msgKeyPressed);
            }
        });
    }

    sendMessage(inputField, msgBox){
        // Send message here
        const chatID = msgBox.querySelector(".details .chatID").innerText;
        const chatObj = activeChats[chatID];
        
        // encryption
        const plainText = inputField.value;
        const cryptKey = chatObj.cryptKey;
        const iv = chatObj.iv;
    
        const cipherText = CryptoJS.AES.encrypt(plainText, cryptKey, {iv: iv});

        chatSocket.send(JSON.stringify({chatID:chatID, cipher_text:`${cipherText}`, type:"sendMsg"}));
        console.log("Sent message");
    };

    receivedMessage(messageData){
        console.log(`Got the Message: ${messageData['cipher_text']}`)
        //access msg box of chat and wipe the input field
    }

    get username() {
        return this.#_username;
    }

    get chatID() {
        return this.#_chatID;
    }

    get cryptKey() {
        return this.#_cryptKey;
    }

    get iv() {
        return this.#_iv;
    }

    get msgBox() {
        return this.#_msgBox;
    }

    get contactDIV() {
        return this.#_contactDIV;
    }
}

let selectedChat = "";

function chatSelected(){
    const chatID = this.querySelector(".chatID").innerText;
    const dashboardContainer = document.querySelector(".dashboardContainer");
    const dummyMsgBox = document.querySelector(".dummyMsgBox");
    const welcomeMsg = document.querySelector(".welcomeMsg");

    const boxChatID = this.querySelector(".chatID").innerText;
    const chatObj = activeChats[boxChatID];
    const contactsMsgBox = chatObj.msgBox;

    dashboardContainer.appendChild(contactsMsgBox);

    if (selectedChat == ""){
        contactsMsgBox.style.display = "block";

        dummyMsgBox.style.display = "none";
        welcomeMsg.style.display = "none";

        selectedChat = chatID;
        this.classList.add("active");
        debug = true;
        // Add .selected class to the contact and display the relevant chat
    } else if (selectedChat == chatID){
        // Hide the msg box and remove selected class off of it

        contactsMsgBox.style.display = "none";

        dummyMsgBox.style.display = "block";
        welcomeMsg.style.display = "block";

        selectedChat = "";
        this.classList.remove("active");
        debug = true;
    } else if (selectedChat !== chatID) {
        // Switch selected chat

        const currentActiveChat = activeChats[selectedChat];
        const currentActiveChatContact = currentActiveChat.contactDIV;
        const currentActiveChatMsgBox = currentActiveChat.msgBox;

        currentActiveChatMsgBox.style.display = "none";
        contactsMsgBox.style.display = "block";

        currentActiveChatContact.classList.remove("active");
        selectedChat = chatID;
        this.classList.add("active");
        debug = true;
    }
}

/* CONDITIIONS TO SEND AN INPUT FROM ENTRY FIELD:
    - Is a current contact selected?
    - Is current contact selected valid?
*/