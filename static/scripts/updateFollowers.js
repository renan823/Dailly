window.onload = ()=>{
    setInterval(()=>{
        data = {"pass": 1}
        fetch("/user/followers/", {
            "method": "POST",
            "cache": "no-cache",
            "body": JSON.stringify(data),
            "header": new Headers({
                "content-type": "application/json"
            })
        })
        .then(response=>{
            return response.json()
        })
        .then(data=>{
            let followers = document.querySelector("#followers")
            followers.innerText = "Seguidores: " + data.followers

            let following = document.querySelector("#following")
            following.innerText = "Seguindo: " + data.following
        })
    }, 5000)
}