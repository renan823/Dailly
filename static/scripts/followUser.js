const followUser = (id)=>{
    data = {user: id}
    fetch("/follower/", {
        "method": "POST",
        "body": JSON.stringify(data),
        "cache": "no-cache",
        "header": new Headers({
            "content-type": "application/json"
        })
    })

}