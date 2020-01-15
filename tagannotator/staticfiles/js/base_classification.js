function get_post(postid){
    posturl='https://www.instagram.com/p/'+postid+'/';
    $.ajax({
        async: false,
        type: "GET",
        global: false,
        dataType: 'html',
        url:posturl,
        data:{},
        success: function(response){
            var metas=$(response).find("meta").prevObject;
            var tags=[];
            for (let i = 0; i < metas.length; i++) {
                curmeta=metas[i];
                var attr = $(curmeta).attr('property');
                if (typeof attr !== typeof undefined && attr !== false) {
                    if(attr=='instapp:hashtags'){
                        tags.push($(curmeta).attr('content'));
                    }
                }
            }
            show_tags(tags);
        } 
    
    });
}
function show_tags(tags){
    $('#classification-holder').empty();
    for (let j =0; j<Math.min(tags.length, 10); j++){
        show_tag(tags[j], j);
    }  
    
    // btns event listeners
    contextbtns=document.getElementsByClassName('btn-context');
    for (var w=0; w<contextbtns.length; w++){
        curbtn=contextbtns[w];
        curbtn.addEventListener("click", function(){
            sleep(300).then(()=>{renderpreview_classification()})
    })}

    // donotuses event listenrs
    xbtns = document.getElementsByClassName('donotuse');
    for (var w=0; w<xbtns.length; w++){
        curxbtn=xbtns[w];
        curxbtn.addEventListener("click", function(){
            sleep(300).then(()=>{donotuse(this)})
    })}
}
function show_tag(tag, tagno){
    labelingpanel=document.getElementById('classification-holder');
    newtagholder=$("#skeleton-tag-holder" ).clone();
    newtagholder.attr('id', 'tag-holder-'+String(tagno));
    newtagholder.addClass('tag-holder');
    newtagholder.find('#tag-text').text(tag);
    newtagholder.appendTo("#classification-holder");
    newtagholder.css('display','');
    newtagholder.css('padding-top','5px');
    newtagholder.css('padding-bottom','5px');
}

function renderpreview_classification(){
    tagholders=document.getElementsByClassName('tag-holder');
    var datapreview=[];
    for (var k=0; k<tagholders.length; k++){
        curtagholder=tagholders[k];
        selection=curtagholder.getElementsByTagName('div')[1].getElementsByTagName('div')[0].getElementsByTagName('div')[0].getElementsByClassName('active');
        if(selection.length!=0){
            tagtext=curtagholder.getElementsByTagName('div')[0].getElementsByTagName('span')[1].innerText;
            context=selection[0].innerText;
            datapreview.push({"tag":tagtext,"context":context});
        }
    }
    document.getElementById('classification-preview').innerText=JSON.stringify(datapreview);
}

function donotuse(xbtn){
    tagholder=xbtn.parentElement.parentElement;
    tagholder.parentNode.removeChild(tagholder);
    renderpreview_classification()
}


function save_classification(){
    tagholders=document.getElementsByClassName('tag-holder');
    taglist=[];
    contextlist=[];
    for (var k=0; k<tagholders.length; k++){
        curtagholder=tagholders[k];
        selection=curtagholder.getElementsByTagName('div')[1].getElementsByTagName('div')[0].getElementsByTagName('div')[0].getElementsByClassName('active');
        if(selection.length!=0){
            tagtext=curtagholder.getElementsByTagName('div')[0].getElementsByTagName('span')[1].innerText;
            context=selection[0].innerText;
            taglist.push(tagtext);
            contextlist.push(context);
        }
    }
    postpk=document.getElementById('img-holder').getAttribute('value');
    $.ajax({
        url:'classification/savetagcontext/'+postpk,
        method: 'POST',
        data: {'tags[]':taglist, 'contexts[]':contextlist}
    });
    sleep(500).then(()=>{show_generation();})
    
}

function show_generation(){
    document.getElementById('classification-save').style.display='none';
    document.getElementById('classification-prompt').style.display='none';
    document.getElementById('classification-div').style.display='none';
    document.getElementById('generation-save').style.display='';
    document.getElementById('generation-prompt').style.display='';
    document.getElementById('generation-div').style.display='';   
    $("input[data-role=tagsinput], select[multiple][data-role=tagsinput]").tagsinput();
}

function show_classification(){
    document.getElementById('classification-save').style.display='';
    document.getElementById('classification-prompt').style.display='';
    document.getElementById('classification-div').style.display='';
    document.getElementById('generation-save').style.display='none';
    document.getElementById('generation-prompt').style.display='none';
    document.getElementById('generation-div').style.display='none';    
}
