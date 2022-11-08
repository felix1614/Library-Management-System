var login_ = document.getElementById("login");
// var register_ = document.getElementById("register");
var button = document.getElementById("btn");

function login() {
    login_.style.left = "50px";
    // register_.style.left = "450px";
    button.style.left = "0";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginValidation() {
    console.log("inside js");
    userName = document.getElementById("userName").value;
    passWord = document.getElementById("passWord").value;
    console.log(userName);

    const datas = { "userDetails": { "username": userName, "password": passWord } };
    csrftoken = getCookie('csrftoken');
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(datas)
    };
    fetch('/home/', options)
        .then(response => {
            if (response.ok) {
                response.json().then(json => {
                    console.log(json);
                })
            }
        });
}