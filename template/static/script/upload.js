function upload(event) {
    if (event.target.value) {
        axios({
            method: 'post',
            url: '/image',
            data: new FormData(document.getElementById("form")),
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(function (response) {
            var message = response.data;
            switch (message["code"]) {
                case 200:
                    var result = document.getElementById("result");
                    result.setAttribute("value", message["url"]);
                    var button = document.getElementById("copy");
                    var clipboard = new ClipboardJS(button);
                    button.click();
                    break;
                case 701:
                    alert(message["message"])
                    break;
            }
        }).catch(function (error) {
            console.log(error);
            alert("服务器出了点问题!");
        }).then(function () {
            var file = document.getElementsByTagName("input")[0];
            file.outerHTML = file.outerHTML;
        });
    }
}