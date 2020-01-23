$(document).ready(function(){
    render_table()
})
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
        render_table();
    }
    }

});
});

function render_table(){
    table=$("#gallery tbody");
    table.empty();
    $.ajax({
        type: "GET",
        url:'../upload/getphotos/',
        dataType: 'json',
        success: function(photosdata){
            photos_list=JSON.parse(photosdata);
            table=$("#gallery tbody");
            table.empty();
            for (var w=0; w<photos_list.length; w++){
                photo=photos_list[w];
                table.append(
                "<tr class='imgrow' id=photo_"+String(photo["pk"])+"><td>"+ String(w+1) +"</td><td><img class='img_preview' src='"+photo["url"] +"'>" + photo["filename"] + "</a><span class='btn trashbtn'><i class='fa fa-trash'></i></span></td></tr>"
                )
            }
            add_deletelistener()
            }
        });

    
}

function add_deletelistener(){
    trashbtns=document.getElementsByClassName('trashbtn');
    for (var w=0; w<trashbtns.length; w++){
        curbtn=trashbtns[w];
        curbtn.addEventListener("click", function(){
            sleep(100).then(()=>{
                delete_row(this)
            })
    })}
}

function delete_row(elem){
    photopk=elem.parentNode.parentNode.id.split('_')[1];
    $.ajax({
        url:'../upload/delete/',
        method: 'POST',
        dataType:'json',
        data: {'photopk':photopk}
        
    });
    sleep(300).then(()=>{
    render_table();});

}


function finish_upload(){
    // make post object for each image 
    $.ajax({
        url:'../upload/createposts/',
        method: 'GET',
        dataType:'json',
        success: function(response){
            result=response['result'];
            if(result){
                window.location.href='../upload/generatetags/1/';
            }
            else{
                console.log('Not enough images uploaded.')
            }
        }
    });
}