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
    var form = document.getElementById("post-form");
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
        if(els[i].className != "special")
            els[i].onclick = (e) => {
                location.href = els[i].getAttribute("href");
            };
    }
}

window.onload = () => {
    parseAllButtonHref();
};

function sendThumb(postId, type) {
    $.ajax({
        url: "/thumb_give/",
        method: "POST",
        data: {
            post: postId,
            type: type
        },
        datatype: "json"
    }).done(function (data) {
        if (data === "1") {

        }
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
    }).done(response => {
        console.log(response);
        area.remove()
    });
}

function commentOnPost(postId) {
    var post = document.getElementById("post_" + postId);
    var area = document.createElement("textarea");
    area.className = "response";
    area.value = "Write your response."
    area.setAttribute("unused", "true");
    area.addEventListener("click", (evt) => {
        if(area.getAttribute("unused") === "true") {
            area.value = "";
            area.setAttribute("unused", "false");
        }
    });
    area.addEventListener("keypress", evt => {
        if(evt.which === 13) {
            sendComment(postId, area)
        }
    })
    post.appendChild(area)
}
