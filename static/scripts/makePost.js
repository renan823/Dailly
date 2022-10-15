const form = document.querySelector("form")
const inputTitle = document.querySelector('#title')
const inputText = document.querySelector('#text')
form.addEventListener("submit", (e)=>{
    e.preventDefault()
    title = inputTitle.value
    text = inputText.value
    if(!text.trim().length == 0 || !title.trim().length == 0){
        let data = {
            title: title,
            text: text
        }
        fetch("/post/new/", {
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
            let icon = 'error'
            let title = 'Ooops...'
            if(data.status == "OK"){
                icon = 'success'
                title = 'Sucesso!'
            }
            Swal.fire({
                icon: icon,
                title: title,
                text: data.msg,
            })
            inputTitle.value = ""
            inputText.value = ""
        })
    }
    
})
