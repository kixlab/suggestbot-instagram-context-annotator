$(document).ready(function(){
     // jQuery AJAX set up
     function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    /////////////////////////////////////////
})

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
  }

$(function () {

$(".js-upload-photos").click(function () {
    $("#fileupload").click();
});

$("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
    $("#modal-progress").modal("show");
    },
    stop: function (e) { /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
        $("#modal-progress").modal("hide");
        // Ensure hide occurs after the fade animation has completed
        setTimeout(function(){$("#modal-progress").modal("hide")}, 1000)
    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
    var progress = parseInt(data.loaded / data.total * 100, 10);
    var strProgress = progress + "%";
    $(".progress-bar").css({"width": strProgress});
    $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
    if (data.result.is_valid) {
        $("#gallery tbody").prepend(
        "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
    }
    }

});

});