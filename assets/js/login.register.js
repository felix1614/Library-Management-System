var login_ = document.getElementById("login");
// var register_ = document.getElementById("register");
var button = document.getElementById("btn");

// function register() {
//     login_.style.left = "-400px";
//     register_.style.left = "50px";
//     button.style.left = "110px";
// }

function login() {
    login_.style.left = "50px";
    // register_.style.left = "450px";
    button.style.left = "0";
}

function setCookie() {
    var User = document.getElementById("userName").value();
    var Pass = document.getElementById("passWord").value();
    console.log(User);
    document.cookie = "myusrname=" + User + ";path=http://localhost/web6pm/";
    document.cookie = "mypsd=" + Pass + ";path=http://localhost/web6pm/";

}