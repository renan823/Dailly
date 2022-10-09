window.onload = ()=>{
    let data = new FormData()
    fetch("/makepost/", {
        "method": "POST",
        "body": {"user": "josias"}
    })
    .then(response=>{
        return response.json()
    })
    .then(data=>{
        console.log(data)
    })
}