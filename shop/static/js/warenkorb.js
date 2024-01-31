let bestellenButtons = document.getElementsByClassName("warenkorb-bestellen");

for(let i=0; i < bestellenButtons.length; i++){
  bestellenButtons[i].addEventListener('click', function() {
    let artikelId = this.dataset.artikel;
    let action = this.dataset.action;
    updateKundenBestellung(artikelId, action)
  })
}

function updateKundenBestellung(artikelId, action){
  let url = "/artikel_backend/"
  console.log("ID: ", artikelId);
  fetch(url,{
    method:'post',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'artikelId':artikelId, 'action':action})
  })
  .then(()=>{
    location.reload()
  })
}