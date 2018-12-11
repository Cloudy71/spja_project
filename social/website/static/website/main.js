function displayPostForm() {
    var form = document.getElementById("post-form");
    form.style.display = "flex";
}

function followUser(username) {
    $.ajax({
        url: "/follow/" + username
    }).done(function (data) {
        if (data === "1") {
            let els = document.getElementsByName("flw_" + username);
            for (let i = els.length - 1; i >= 0; i--) {
                els[i].className = "date_button gray";
                els[i].onclick = ev => {
                    stopFollowingUser(username);
                };
                els[i].innerText = "Stop following";
            }
        }
    });
}

function stopFollowingUser(username) {
    $.ajax({
        url: "/stop-follow/" + username
    }).done(function (data) {
        if (data === "1") {
            let els = document.getElementsByName("flw_" + username);
            for (let i = els.length - 1; i >= 0; i--) {
                els[i].className = "date_button blue";
                els[i].onclick = ev => {
                    followUser(username);
                };
                els[i].innerText = "Follow";
            }
        }
    });
}
