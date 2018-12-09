function showPage(url) {
    $.ajax({
        url: "/" + url
    }).done(function (data) {
        let container = document.getElementById("container");
        container.innerHTML = data;
        container.style.top = (window.innerHeight/2 - container.offsetHeight/2)+"px";
    });
}

showPage("login");
