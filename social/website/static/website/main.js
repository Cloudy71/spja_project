function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function displayPostForm() {
    let form = document.getElementById("post-form");
    form.style.display = "flex";
}

$(document).ready(function () {
    $.ajaxSetup({
        headers: /*{'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')}*/{"X-CSRFToken": getCookie("csrftoken")}
    });
});

function sendFollow(username, type) {
    //{ 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }
    $.ajax({
        url: "/follow/",
        method: "POST",
        data: {
            user: username,
            type: type
        },
        datatype: "json"
    }).done(function (data) {
        if (data === "1") {
            if (type === 0) {
                let els = document.getElementsByName("flw_" + username);
                for (let i = els.length - 1; i >= 0; i--) {
                    els[i].className = "date_button gray";
                    els[i].onclick = ev => {
                        sendFollow(username, 1);
                    };
                    els[i].innerText = "Unfollow";
                }
            } else {
                let els = document.getElementsByName("flw_" + username);
                for (let i = els.length - 1; i >= 0; i--) {
                    els[i].className = "date_button blue";
                    els[i].onclick = ev => {
                        sendFollow(username, 0);
                    };
                    els[i].innerText = "Follow";
                }
            }
        }
    });
}

function parseAllButtonHref() {
    let els = document.getElementsByTagName("BUTTON");
    for (let i = 0; i < els.length; i++) {
        if (els[i].className !== "special")
            els[i].onclick = (e) => {
                location.href = els[i].getAttribute("href");
            };
    }
}

window.onload = () => {
    parseAllButtonHref();
};

function sendThumb(element, postId, type) {
    $.ajax({
        url: "/thumb-give/",
        method: "POST",
        data: {
            post: postId,
            type: type
        },
        datatype: "json"
    }).done(function (data) {
        if (data.startsWith("0")) {
            return;
        }
        let json = JSON.parse(data);
        let buttons = element.parentNode.getElementsByTagName("DIV");
        buttons[0].getElementsByTagName("LABEL")[0].innerText = json["up"];
        buttons[1].getElementsByTagName("LABEL")[0].innerText = json["down"];
        if (type === -1) {
            buttons[0].className = "button" + (buttons[0].className.indexOf("mini") >= 0 ? " mini" : "");
            buttons[0].onclick = () => {
                sendThumb(element, postId, 0);
            };
            buttons[0].getElementsByTagName("IMG")[0].src = img_thumb_up_n;
            buttons[1].className = "button" + (buttons[1].className.indexOf("mini") >= 0 ? " mini" : "");
            buttons[1].onclick = () => {
                sendThumb(element, postId, 1);
            };
            buttons[1].getElementsByTagName("IMG")[0].src = img_thumb_down_n;
        } else if (type === 0) {
            buttons[0].className = "button" + (buttons[0].className.indexOf("mini") >= 0 ? " mini" : "") + " g_used";
            buttons[0].onclick = () => {
                sendThumb(element, postId, -1);
            };
            buttons[0].getElementsByTagName("IMG")[0].src = img_thumb_up;
            buttons[1].className = "button" + (buttons[1].className.indexOf("mini") >= 0 ? " mini" : "");
            buttons[1].onclick = () => {
                sendThumb(element, postId, 1);
            };
            buttons[1].getElementsByTagName("IMG")[0].src = img_thumb_down_n;
        } else if (type === 1) {
            buttons[0].className = "button" + (buttons[0].className.indexOf("mini") >= 0 ? " mini" : "");
            buttons[0].onclick = () => {
                sendThumb(element, postId, 0);
            };
            buttons[0].getElementsByTagName("IMG")[0].src = img_thumb_up_n;
            buttons[1].className = "button" + (buttons[1].className.indexOf("mini") >= 0 ? " mini" : "") + " r_used";
            buttons[1].onclick = () => {
                sendThumb(element, postId, -1);
            };
            buttons[1].getElementsByTagName("IMG")[0].src = img_thumb_down;
        }
        console.log(element.parentNode);
    });

    /*$.post("/thumb_give/", {post: postId, type: type}, (data) => {

    });*/
}

function sendComment(postId, area) {
    $.ajax({
        url: "/response",
        method: "POST",
        data: {
            content: area.value,
            main_post: Number(postId),
        },
        datatype: "json"
    }).done(() => {
        area.value = "";
    });
}

function createMiniThumb(type, postId, used, num) {
    let button = document.createElement("DIV");
    let img = document.createElement("IMG");
    let label = document.createElement("LABEL");
    button.className = "button mini" + (used ? " " + (type === 0 ? "g" : "r") + "_used" : "");
    button.onclick = () => {
        sendThumb(button, postId, used ? -1 : type);
    };
    img.src = img_thumb_up.substr(0, img_thumb_up.lastIndexOf("/")) + "/thumb_" + (type === 0 ? "up" : "down") + (!used ? "_n" : "") + ".png";
    img.width = "14";
    label.innerText = num;
    button.appendChild(img);
    button.appendChild(label);
    return button;
}

function createComment(post) {
    let response = document.createElement("div");
    let content = document.createElement("div");
    let user = document.createElement("a");
    let picture = document.createElement("div");
    let reactions = document.createElement("DIV");
    user.className = "whole_name";
    content.innerText = post.content;
    content.className = "comment_content";
    user.href = "/profile/" + post.login;
    user.innerText = post.author;
    picture.className = "profile_picture";
    response.className = "comment";
    picture.style.width = "24px";
    picture.style.height = "24px";
    reactions.className = "reactions_mini";
    response.appendChild(picture);
    response.appendChild(user);
    response.appendChild(content);
    response.appendChild(reactions);

    let thumb_up = createMiniThumb(0, post.id, post.thumb_ups[1], post.thumb_ups[0]);
    reactions.appendChild(thumb_up);
    let thumb_down = createMiniThumb(1, post.id, post.thumb_downs[1], post.thumb_downs[0]);
    reactions.appendChild(thumb_down);

    return response;
}

function createCommentList(responses) {
    console.log();
    let posts = JSON.parse(responses);
    return posts.map(post => createComment(post));
}

function createComments(postId, posts) {
    let area = document.createElement("textarea");
    let post = document.getElementById("post_" + postId);
    let responses = document.createElement("div");
    area.className = "response";
    area.value = "Write your response.";
    area.setAttribute("unused", "true");
    responses.appendChild(area);
    responses.className = "messages";
    createCommentList(posts).forEach(r => responses.appendChild(r));

    area.addEventListener("click", (evt) => {
        if (area.getAttribute("unused") === "true") {
            area.value = "";
            area.setAttribute("unused", "false");
        }
    });
    area.addEventListener("keydown", evt => {
        if (evt.which === 13) {
            sendComment(postId, area);
        }
    });
    post.appendChild(responses);
}

function commentOnPost(postId) {
    let post = document.getElementById("post_" + postId);
    if (post.getAttribute("comments") === null)
        post.setAttribute("comments", "true");
    else
        return;

    $.ajax({
        url: "/response/" + postId,
        method: "GET"
    }).done(resp => createComments(postId, resp))
}
