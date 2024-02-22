const transitions = [...document.getElementsByClassName("transition")]

transitions.map(transition => {
  transition.addEventListener("click", e => {
    e.preventDefault()
    let url = transition.dataset.url
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, change state!'
    }).then(result => {
      if (result.isConfirmed) {
        changeState(url).then(response => {
          if (response.hasOwnProperty("error")) {
            throw new Error(response.error)
          }
          Swal.fire(
            {'icon': 'success', 'title': 'Success', 'text': response.message}
          ).then(result => {
            window.location.reload();
          })
        }).catch(error => {
          Swal.fire(
            {'icon': 'error', 'title': 'Transition', 'text': error}
          )
        })
      }
    })
  })
})

const changeState = async url => {
  let response = await fetch(url)
  return await response.json()
}