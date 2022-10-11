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
        results.innerHTML = ""
    })
}


getPosts()