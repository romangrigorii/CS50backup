
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#profile').addEventListener('click', () => load_posts("profile"));
    document.querySelector('#mainpage').addEventListener('click', () => load_posts("mainpage"));
    document.querySelector('#following').addEventListener('click', () => load_posts("following"));
    document.querySelector('#filledsub').addEventListener('click', () => {
        make_a_post();
        load_posts("profile");
    });
    load_posts("profile");
    return false;
})


function leave_a_like(postid) {
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid,
        })
    })
    .then(result => {
        console.log('successful click on post ' + postid);
        // console.log(result);
        //  alert('g');
    });
    load_posts("profile");
    return false;
}

function gotoprofile(accid) {
    fetch('loadpage/profile/' + accid, {
        method: 'GET',
    })
    .then(response => {return response.json()})
    .then(response => {
        console.log(accid);
        console.log(response);
        return accid;
    })
    return false;
}


function make_a_post(){
    fetch('/makepost', {
        method: 'POST',
        body: JSON.stringify({
            message : document.querySelector('#newpost').value, // message is the name by which this value will be referenced in views.py
        })
    })
    .then(response => {return response.json()}) // we expect some response apon making a post
    .then(result => {console.log(result);}) // we then log the result
    document.querySelector('#newpost').value = "";
    return false;
}

function load_posts(posttype){
    
    fetch("/loadpage/" + posttype)
    .then(response=>response.json())
    .then(posts  => {
        console.log(posts[0])
        document.querySelector("#posts-view").innerHTML = "";
        
        posts[1].forEach((post) => {
            const divpost = document.createElement('div');   
            divpost.id = "postlist";

            const divuser = document.createElement('div');  
            divuser.innerHTML += '<b>' + post.user + '</b> posted on ' + post.timestamp;
            divuser.id = post.poster;
            divuser.className = "userinpost";
            divpost.append(divuser);

            const img1 = document.createElement('img');
            img1.src = posts[0].pictureurl;
            img1.id = "profpicsmall";
            divpost.append(img1);
            
            const divtext = document.createElement('ptr'); 
            divtext.innerHTML = post.message;
            divpost.append(divtext);
            divpost.style.border = "ridge";
            divpost.style.borderRadius = '6px';

            divpost.innerHTML = divpost.innerHTML + "<br>";
            divpost.innerHTML += (post.likes).length + " "; 
            const img2 = document.createElement('img'); 
            img2.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/1200px-Heart_coraz%C3%B3n.svg.png";
            img2.className = "likeid";
            img2.id = post.id;
            divpost.append(img2);

            let commentstext = document.createElement('ptr'); 
            commentstext.id = "commentstext";
            commentstext.innerHTML = "Comments";
            commentstext.addEventListener("click", () => {
                console.log('open comments');
                alert('aaag');
                // read_comments(post.id);                    
            });

            divpost.innerHTML +=  "  " + (post.comments).length + " ";
            divpost.append(commentstext);

            document.querySelector("#posts-view").append(divpost);
            document.querySelector("#posts-view").innerHTML += "<br>";
            console.log(post);
        })

        document.querySelectorAll(".likeid").forEach((unit) => {
            unit.addEventListener("click", () => {
                leave_a_like(unit.id);
            })
        })

        document.querySelectorAll(".userinpost").forEach((unit) => {
            unit.addEventListener("click", () => {
                document.querySelector('#userinfo').style.display = 'block';
                document.querySelector('#postsubmit').style.display = 'none';
                if (gotoprofile(unit.id)) {
                    document.querySelector('#postsubmit').style.display = 'block';
                } else {
                    const follow = document.createElement('button');  
                    follow.value = "Follow";
                    follow.style = "color:blue";
                    document.querySelector("folunfol-view").append(follow);
                }
                const div = document.createElement('div');

                let lenfollowers = 0;
                let lenfollowing = 0;
                if (posts[0].followers){
                    lenfollowers = (posts[0].followers).length;
                }
                if (posts[0].following){
                    lenfollowers = (posts[0].following).length;
                }
                document.querySelector("#followerinfo").innerHTML = "<b>followers:</b> " + lenfollowers +  "  <b>following:</b> " + lenfollowing;
            })
        })


        if (posttype == 'profile'){       
            document.querySelector('#userinfo').style.display = 'block';

            document.querySelector('#postsubmit').style.display = 'block';
            
            const div = document.createElement('div');

            let lenfollowers = 0;
            let lenfollowing = 0;
            if (posts[0].followers){
                lenfollowers = (posts[0].followers).length;
            }
            if (posts[0].following){
                lenfollowers = (posts[0].following).length;
            }

            document.querySelector("#followerinfo").innerHTML = "<b>followers:</b> " + lenfollowers +  "  <b>following:</b> " + lenfollowing;

        } else {
            document.querySelector('#userinfo').style.display = 'none';
            document.querySelector('#postsubmit').style.display = 'none';
        }
        return false;
    })
    return false;
}