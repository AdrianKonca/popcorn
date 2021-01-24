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

function parseResponse(response) {
    if (response.status === 200) {
        return response.json();
    } else {
        return null;
    }
}

function displaySignupMessage(body) {
    if (body === null) {
        return;
    }
    const result = body.result;
    const message = body.message;
    const newsletterSignupError = document.getElementById("newsletter-signup-error");
    const emailInput = document.getElementById("inputEmailNewsletter");
    
    if (result == "Success") {
        newsletterSignupError.innerHTML = "";
        emailInput.classList.remove("is-invalid");
        const newItem = document.createElement('div');
        newItem.innerHTML = message;    
        emailInput.parentNode.replaceChild(newItem, emailInput);
    }
    else {
        newsletterSignupError.innerHTML = message;
        emailInput.classList.add("is-invalid");
    }
}

function signup(event) {
    const emailInput = document.getElementById("inputEmailNewsletter");
    const email = emailInput.value;
    const csrftoken = getCookie('csrftoken');
    fetch('/newsletter/signup',
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({email: email})
        }
    ).then(response => parseResponse(response)).then(body => displaySignupMessage(body));
}

window.onload = function () {
    const newsletterSignupButton = document.getElementById("newsletter-signup");
    newsletterSignupButton.addEventListener('click', signup);
}
