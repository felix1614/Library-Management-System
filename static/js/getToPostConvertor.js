//('#postLink').click(function(req) {
//    req.preventDefault();
//    var form = ('<form method="POST" action="/users/"></form>');
//    (document.body).append(form);
//    form.append('<input type="hidden" name="id" value="4"/>')
//    form.submit();
//});

function postForm(req) {
    // window.location.href = "/";
    var formData = document.getElementById('postChanger');
    if (req == 'bookArrival') {
        formData.setAttribute("action", "/%5Escan/$%5Ebooks/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "bookArrival");
        formData.appendChild(formElement);
        formData.submit();
    } else if (req == 'newUser') {
        formData.setAttribute("action", "/%5Escan/$%5Eusers/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "newUser");
        formData.appendChild(formElement);
        formData.submit();

    } else if (req == 'addUser') {
        formData.setAttribute("action", "/%5Escan/$%5Eupdate/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "addUser");
        formData.appendChild(formElement);
        formData.submit();
    } else if (req == 'updateUser') {
        formData.setAttribute("action", "/%5Escan/$%5Eupdate/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "updateUser");
        formData.appendChild(formElement);
        formData.submit();
        var formData1 = document.getElementById('uname');
        var formElement1 = document.createElement("input");
    } else if (req == 'addBook') {
        formData.setAttribute("action", "/%5Escan/$%5Eupdate/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "addBook");
        formData.appendChild(formElement);
        formData.submit();
    }
}