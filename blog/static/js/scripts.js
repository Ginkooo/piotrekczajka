function popUp(status, msg, redirect) {
    let color = 'green'
    switch (status) {
        case 'ok':
            color = 'green'
            break
        case 'fail':
            color = 'red'
            break
        default:
            color = 'blue'
    }
    let popup = document.querySelector('#popup-msg')
    let span = document.querySelector('#popup-msg > span')
    popup.style.background = color
    popup.style.display = 'block'
    span.innerHTML = msg
    setTimeout(function () {
        popup.style.display = 'none'
        if (redirect) {
            window.location = redirect
        }
    }, 2000)
}

function asyncPost(url, data, success, error) {
  var http = new XMLHttpRequest()
  var params = JSON.stringify(data)
  http.open('POST', url, true)

  http.setRequestHeader('Content-type', 'application/json')
  http.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))

  http.onreadystatechange = function () {
    if (http.readyState !==4) {
      return
    }
    if (http.status >= 200 && http.status < 300) {
      success(http)
      return
    }
    error(http)
  }

  http.send(params)
}
