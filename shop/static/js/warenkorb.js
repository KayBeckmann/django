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

//KASSE
let formular = document.getElementById('formular')
let gesamtpreis = document.getElementById('gesamtpreis').value

formular.addEventListener('submit', function(e){
  e.preventDefault()
  document.getElementById('formular-button').classList.add('d-none')
  document.getElementById('bezahlen-info').classList.remove('d-none')
})

document.getElementById('bezahlen-button').addEventListener('click', function(e){
  submitFormular();
})

function submitFormular(){
  let benutzerdaten = {
    'name': formular.inputName.value,
    'email': formular.inputEmail.value,
    'gesamtpreis': gesamtpreis
  }
  let lieferadresse = {
    'adresse':formular.inputAdresse.value,
    'plz':formular.inputPlz.value,
    'stadt':formular.inputStadt.value,
    'land':formular.inputLand.value,
  }

  let url = "/bestellen/"
  
  fetch(url,{
    method:'post',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'benutzerdaten':benutzerdaten, 'lieferadresse':lieferadresse})
  })
  .then(()=>{
    window.location.href="/"
  })
}