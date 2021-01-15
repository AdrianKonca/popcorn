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

function updateVoteButtonStyle(result, voteUpButton, voteDownButton) {
    if (result === 'up') {
        voteUpButton.classList.add('vote-up')
        voteDownButton.classList.remove('vote-down')
    } else if (result === 'down') {
        voteUpButton.classList.remove('vote-up')
        voteDownButton.classList.add('vote-down')
    } else if (result === 'default') {
        voteUpButton.classList.remove('vote-up')
        voteDownButton.classList.remove('vote-down')
    }
}

function updateCommentVoteValue(body, id) {
    if (body === null) {
        return;
    }
    const voteCount = body.count;
    const result = body.action;
    document.getElementById('comment-vote-count-' + id.toString()).innerHTML = `Głosy: ${voteCount}`;
    const voteUpButton = document.getElementById('comment-vote-button-up-' + id.toString());
    const voteDownButton = document.getElementById('comment-vote-button-down-' + id.toString());
    updateVoteButtonStyle(result, voteUpButton, voteDownButton);
}

function updateRecipeVoteValue(body) {
    if (body === null) {
        return;
    }
    const voteCount = body.count;
    const result = body.action;

    document.getElementById('recipe-vote-count').innerHTML = `Głosy: ${voteCount}`;
    const voteUpButton = document.getElementById('recipe-vote-button-up')
    const voteDownButton = document.getElementById('recipe-vote-button-down')
    updateVoteButtonStyle(result, voteUpButton, voteDownButton);
}

function parseResponse(response) {
    if (response.status === 200) {
        return response.json();
    } else {
        return null;
    }
}

function voteComment(event) {
    let idParts = event.target.id.split('-');
    let id = idParts[idParts.length - 1];
    let action = idParts[idParts.length - 2];
    const csrftoken = getCookie('csrftoken');
    fetch('/comments/vote/' + id.toString(),
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({action: action})
        }
    ).then(response => parseResponse(response)).then(body => updateCommentVoteValue(body, id));
}

function voteRecipe(event) {
    let idParts = event.target.id.split('-');
    let action = idParts[idParts.length - 1];
    const csrftoken = getCookie('csrftoken');
    fetch(window.location.pathname + '/vote',
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({action: action})
        }
    ).then(response => parseResponse(response)).then(body => updateRecipeVoteValue(body));
}

window.onload = function () {
    commentsVotes = document.querySelectorAll("[id^='comment-vote-button']")
    commentsVotes.forEach(commentVoteButton => {
        commentVoteButton.addEventListener('click', voteComment)
    });

    recipeVotes = document.querySelectorAll("[id^='recipe-vote-button']")
    recipeVotes.forEach(recipeVoteButton => {
        recipeVoteButton.addEventListener('click', voteRecipe)
    });
}