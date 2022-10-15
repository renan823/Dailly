const results = document.querySelector("#posts")
const getPosts =  ()=>{
    data = {"pass": 1}
    fetch("/post/get/", {
        "method": "POST",
        "body": JSON.stringify(data),
        "cache": "no-cache",
        "header": new Headers({
            "content-type": "application/json"
        })
    })
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        postList = data.posts
        for(let i in postList){
            let posts = postList[i]
            for(let j in posts){
                let post = posts[j]
                
                let box = document.createElement("div")
                box.classList.add("post")

                let userName = document.createElement("h5")
                userName.innerText = post.user
                box.appendChild(userName)


                let title = document.createElement("h2")
                title.innerText = post.title
                box.appendChild(title)

                let text = document.createElement("p")
                text.innerText = post.text
                box.appendChild(text)

                results.appendChild(box)
            }
        }
    })
}


getPosts()
