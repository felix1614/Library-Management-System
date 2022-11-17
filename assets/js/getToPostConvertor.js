//('#postLink').click(function(req) {
//    req.preventDefault();
//    var form = ('<form method="POST" action="/users/"></form>');
//    (document.body).append(form);
//    form.append('<input type="hidden" name="id" value="4"/>')
//    form.submit();
//});

function postForm(req) {
    // window.location.href = "/";
    if (typeof(req) != 'string'){
    reqKey = req[1];
    req = req[0];
    }
    else {
    req = req;
    }
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

//        var uname = document.getElementById('uname').innerText;
        var formElement1 = document.createElement("input");
        formElement1.setAttribute("type", "hidden");
        formElement1.setAttribute("name", "val");
        formElement1.setAttribute("value", `${reqKey}`);
        formData.appendChild(formElement);
        formData.appendChild(formElement1);
        formData.submit();
    } else if (req == 'addBook') {
        formData.setAttribute("action", "/%5Escan/$%5Eupdate/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "addBook");
        formData.appendChild(formElement);
        formData.submit();
    } else if (req == 'rentPage') {
        formData.setAttribute("action", "/%5Escan/$%5Erentform/$");
        var formElement = document.createElement("input");
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", `rentBook-${reqKey}`);
        formData.appendChild(formElement);
        formData.submit();
    } else if (req == 'RentBook') {
        formData.setAttribute("action", "/%5Escan/$%5Esave/$");
        var formElement = document.createElement("input");
        var formObject = document.createElement("input");
        var bookId = document.getElementById('bookID').value;
        var Duration = document.getElementById('dur').value;
//        var dur = Duration.options[Duration.selectedIndex].text;
        var userName = document.getElementById('userName').value;
        var durTime = document.getElementById('duration').value;
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "rental");

        formObject.setAttribute("type", "hidden");
        formObject.setAttribute("name", "val");
        formObject.setAttribute("value", `{'bookId':'${bookId}','rentDur':'${Duration}','userName':'${userName}','duration':'${durTime}'}`);

        formData.appendChild(formElement);
        formData.appendChild(formObject);
        formData.submit();
    }else if (req == 'RentForm') {
        formData.setAttribute("action", "/%5Escan/$%5Erentform/$");
        var formElement = document.createElement("input");
        var formObject = document.createElement("input");
        var bookId = document.getElementById('Book-id').value;
//        var Duration = document.getElementById('dur').value;
        var userName = document.getElementById('userName').value;
//        var durTime = document.getElementById('duration').value;
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "rentalForm");

        formObject.setAttribute("type", "hidden");
        formObject.setAttribute("name", "val");
        formObject.setAttribute("value", `{'bookId':'${bookId}','userName':'${userName}'}`);

        formData.appendChild(formElement);
        formData.appendChild(formObject);
        formData.submit();
    } else if (req == 'scan') {
        formData.setAttribute("action", "/%5Escan/$%5Escan/$");
        var formElement = document.createElement("input");
        var qty = document.getElementById('quantity').value;
        if (qty == ""){
        qty = 20
        }
        else{
        qty = qty
        }
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "scan");

        var formObject = document.createElement("input");
        formObject.setAttribute("type", "hidden");
        formObject.setAttribute("name", "val");
        formObject.setAttribute("value", `{'qty':'${qty}'}`);
        formData.appendChild(formElement);
        formData.appendChild(formObject);
        formData.submit();
} else if (req == 'ReturnBook') {
        formData.setAttribute("action", "/%5Escan/$%5Esave/$");
        var formElement = document.createElement("input");
        var formObject = document.createElement("input");
        var bookId = document.getElementById('Book-id').value;
//        var Duration = document.getElementById('dur').value;
        var userName = document.getElementById('userName').value;
//        var durTime = document.getElementById('duration').value;
        formElement.setAttribute("type", "hidden");
        formElement.setAttribute("name", "key");
        formElement.setAttribute("value", "returnBook");

        formObject.setAttribute("type", "hidden");
        formObject.setAttribute("name", "val");
        formObject.setAttribute("value", `{'bookId':'${bookId}','userName':'${userName}'}`);

        formData.appendChild(formElement);
        formData.appendChild(formObject);
        formData.submit();
    }
}

function imgConvertor ()  {
    var file = document.querySelector('input[type=file]')['files'][0];
    var reader = new FileReader();
    var baseString;
    reader.onloadend = function () {
        baseString = reader.result;
        console.log(baseString);
        document.getElementById("hiddenImage").value = baseString;
    };
    reader.readAsDataURL(file);

}