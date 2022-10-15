const input = document.querySelector("input")
const results = document.querySelector("#results")
input.addEventListener("keyup", ()=>{
    let name = input.value
    if(name.trim().length != 0){
        data = {name: name}
        fetch("/search/", {
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
            let users = data.users
            for(let i in users){
                let user = users[i]

                let box = document.createElement("div")
                box.classList.add("user")

                let userName = document.createElement("h4")
                userName.innerText = user.name
                box.appendChild(userName)

                let followButton = document.createElement("button")
                followButton.setAttribute("id", user._id)
                followButton.innerText = "Seguir"
                followButton.addEventListener('click', ()=>{
                    let id = user._id
                    followUser(id)
                    results.removeChild(followButton.parentElement)
                })
                box.appendChild(followButton)

                results.appendChild(box)
            }
        })
    }
    else{
        results.innerHTML = ""
    }
})
