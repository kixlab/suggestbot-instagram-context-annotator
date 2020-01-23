function generate_data(){
    tagholders=document.getElementsByClassName('tag-holder');
    var data=[];
    for (var k=0; k<tagholders.length; k++){
        curtagholder=tagholders[k];
        tagpk=curtagholder.getElementsByClassName('tagtext')[0].getElementsByTagName('span')[0].id.split('_')[1];
        selection=curtagholder.getElementsByClassName('btn-context active');
        
        contexts=[]
        if(selection.length!=0){
            for (var i=0;i<selection.length;i++){
                contextpk=selection[i].id.split('_')[2];
                contexts.push(contextpk)
            }
            data.push({hashtag:tagpk,context:contexts});
        }
        
    }
    return data
}

function save_labels(postorder){
    tagcontextdata=generate_data()
    if(tagcontextdata.length<5){
        window.alert("select at least one context labels for 5+ hashtags")
    }else{
        $.ajax({
            url:'',
            method: 'POST',
            dataType: 'json',
            data:{'mappings':JSON.stringify(tagcontextdata)},
            success: function(response){
                if(response["result"]){
                    if(postorder>4){
                        window.location.href='../../classification/finish/'
                    }
                    else{
                        window.location.href='../'+String(postorder+1)+'/';
                    }
                }                
            }
        });
    }
}