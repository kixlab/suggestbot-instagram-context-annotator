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
    donotusebtns= document.getElementsByClassName('donotuse');
    for (var w=0; w<donotusebtns.length; w++){
        curxbtn=donotusebtns[w];
        curxbtn.addEventListener("click", function(){
            sleep(300).then(()=>{renderpreview_classification()
            })
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
    data=generate_data();
    previewtable=document.getElementById('preview-table');
    previewnodata=document.getElementById('preview-nodata');
    if (data.length!=0){
        previewnodata.style='display:none;'
        previewtbody=document.getElementById('preview-rows');
        previewtbody.innerHTML='';
        for(var i=0;i<data.length;i++){
            hashtagtext=data[i]["hashtag"]
            contextlabels=data[i]["context"].join(", ");
            newrow=previewtbody.insertRow(previewtbody.rows.length);
            newno=newrow.insertCell(0);
            newhashtag=newrow.insertCell(1);
            newcontexts=newrow.insertCell(2);
            newno.appendChild(document.createTextNode(String(i+1)));
            newhashtag.appendChild(document.createTextNode('#'+hashtagtext));
            newcontexts.appendChild(document.createTextNode(contextlabels));
        }
        previewtable.style='display:block';
    }
    else{
        previewtable.style='display:none;';
        previewnodata.style='display:block';
    }

}

function generate_data(){
    tagholders=document.getElementsByClassName('tag-holder');
    var data=[];
    for (var k=0; k<tagholders.length; k++){
        curtagholder=tagholders[k];
        tagtext=curtagholder.getElementsByClassName('tagtext')[0].getElementsByTagName('span')[1].innerText;
        selection=curtagholder.getElementsByClassName('contextbtns')[0].firstElementChild.firstElementChild.getElementsByClassName('active');
        donotuse=curtagholder.getElementsByClassName('donotuse')[0].firstElementChild;
        if(donotuse.checked){
            contexts=[]
            if(selection.length!=0){
                for (var i=0;i<selection.length;i++){
                    context=selection[i].innerText;
                    contexts.push(context)
                }
                data.push({hashtag:tagtext,context:contexts});
            }
        }
    }
    return data
}

function save_classification(){
    tagcontextdata=generate_data()
    console.log(data)
    $.ajax({
        url:'savetagcontext/',
        method: 'POST',
        dataType: 'json',
        data: {'tagcontext':JSON.stringify(tagcontextdata), 'madeby':'post'}
    });
    
}