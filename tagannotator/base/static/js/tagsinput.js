$(document).ready(function(){
    document.getElementById("hashtag_input")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        add_tag();
    }
});
    show_hashtags(hashtags);
})

function show_hashtags(hashtags){
    if(hashtags.length==0){
        $('#preview-nodata').css({display:'block'});
        $('#hashtag-preview').css({display:'none'});
    }
    else{        
        hashtagsholder=document.getElementById('hashtag-preview')
        hashtagsholder.innerHTML='';
        for (var k=0; k<hashtags.length; k++){
            curtag=hashtags[k][0];
            newtag=document.createElement("span");
            newtag.classList.add("hashtag")
            newtag.innerHTML='#'+curtag+'<span class="btn deletebtns" onclick="remove_tag(this)" style="padding:3px;padding-top:0px;color:blue;"><i class="fa fa-times"></i></span>'
            hashtagsholder.appendChild(newtag);
        }        
        $('#preview-nodata').css({display:'none'});
        $('#hashtag-preview').css({display:'block'});

    }
}

function add_tag(){
    newtagtext=$('#hashtag_input').val().replace('#','');
    console.log(newtagtext)
    duplicate=false;
    for (var i=0;i<hashtags.length;i++){
        hashtag=hashtags[i];
        if(hashtag[0]==newtagtext){
            duplicate=true;
            break;
        }
    }
    if (duplicate){
        window.alert("no duplicated tags allowed")
    }else{
        if(newtagtext.length<2){
            window.alert("hashtag should have at least 2 characters")
        }else{
        hashtags.push([newtagtext, 'user'])
    }
}
    show_hashtags(hashtags)
    $('#hashtag_input').val('')

}

function remove_tag(elem){
    curtag=elem.parentNode;
    curtagtext=curtag.innerText.substr(1);
    for (var i=0;i<hashtags.length;i++){
        if(hashtags[i][0]==curtagtext){
            hashtags.splice(i,1);
        }
    }
    show_hashtags(hashtags);
}


function save_hashtags(postorder){
    if(hashtags.length>4){
        console.log(hashtags)
    //save hashtags
        $.ajax({
            url:'',
            method: 'POST',
            dataType:'json',
            data: {'hashtags':JSON.stringify(hashtags)},
            success: function(response){
                if(response["result"]){
                    if(postorder>4){
                        window.location.href='../../classification/1/'
                    }
                    else{
                        window.location.href='../'+String(postorder+1)+'/';
                    }
                }                
            }
        });  
    }else{
        window.alert('5 or more hashtags needed. ');
    }
}