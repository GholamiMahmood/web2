// methode pour la fonctionalité A5
function creerTableau (donnees){
    var liste = [];
    var liste1 = [];
    var liste2 = [];
    for (let i = 0; i < donnees.length; i++) {
        var nomArrondi = donnees[i].nom_arround;
        var nomQuart = donnees[i].nom_qr;
        var list = [ nomArrondi, nomQuart ]        
        liste.push(list);        
    }
    liste = liste.sort();
    liste.push(["" , ""]);
    var ancienArron = [];
    var ancienQuart = [];
    var cnt = 1;
    for (var i = 0; i < liste.length; i++) {
        var currentArron = liste[i][0];
        var currentQuart = liste[i][1];
        if(i == 0){
            ancienArron = currentArron;
            ancienQuart = ancienQuart;
        }else{
            if ( currentQuart != ancienQuart ) {
                liste1 = [ ancienArron , ancienQuart ,  cnt];
                liste2.push(liste1);
                cnt = 1;               
            }else{
                cnt = cnt + 1;               
           }
           ancienArron = currentArron;
           ancienQuart = currentQuart;
        }        
    }    
    return liste2;
}

function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

function generateTable(table, data) {
    
    for (let element of data) {
      let row = table.insertRow();
      for (key in element) {
        let cell = row.insertCell();
        let text = document.createTextNode(element[key]);
        cell.appendChild(text);
        
      }
    }    
 }

 function creerListQuartier(data) {
    var listQuartier = [];
    for (let ligne of data) {      
      for (element in ligne) {
          if (element == 1){
              let text = document.createTextNode(ligne[element]);              
              listQuartier.push(text.textContent);              
          }          
      }
    }
    // console.log(listQuartier);
    return listQuartier;    
 } 

// Fonctionalité A5
 function chercher() {
    var premierDate = document.getElementById("premiere-date").value;
    var deuxiemeDate = document.getElementById("deuxieme-date").value;
    function effacer()
    {
        document.getElementById('tab').innerHTML = "";
    }
    effacer();
    fetch(`${window.origin}/declarations?du=${premierDate}&au=${deuxiemeDate}`, {
        method: 'GET',        
        headers: {
            'Accept': 'application/json'            
        }        
    })
    .then((response) => {        
        if (response.status == 200) {  
            return response.text();
        }
        else
        {
            throw `error with status ${response.status}`;
        }
    })
    .then(donnees => {
                
        var data = JSON.parse(donnees);
        data = creerTableau( data);
        let table = document.querySelector("table");
        let head = Object.keys({"Arrondissement":"","Quartier":""," Nombre de declarations":""});
        
        generateTableHead(table, head);
        generateTable(table, data);
        // 
        function initialiserlist()
        {
            document.getElementById('subject').innerHTML = "";
        }
        initialiserlist();
        //Fonctionalité A6
        var listQuartier = creerListQuartier(data);
        var idAdresse = document.getElementById("subject");
        subject.disabled = false;
        button.disabled = false;
        suprimId.disabled = false;
        for (var i = 0; i < listQuartier.length; i++) {
            idAdresse.options[idAdresse.options.length] = new Option(listQuartier[i], listQuartier[i]);
          }        
    })                                  
    .catch((exception) => {
        console.log(exception);
    });     
  }
  
  // Fonctionalité A6
  function changerQuartier() {
    var quartier = document.getElementById("subject").value;
    var premierDate = document.getElementById("premiere-date").value;
    var deuxiemeDate = document.getElementById("deuxieme-date").value;
    fetch(`${window.origin}/api/declarationsquartiers?quartiers=${quartier}&date1=${premierDate}&date2=${deuxiemeDate}`, {
        method: 'GET',                
        headers: {
            'Accept': 'application/json',
            'Content-Type' : 'application/json'            
        }             
    })
    .then((response) => {
        if (response.status == 200) {                                
            return response.text();
        }
        else
        {
            throw `error with status ${response.status}`;
        }
    })
    .then(donnees => {
        var url = '/infoquartier';
        var myWindow = window.open(url, "", "width=800,height=600");
        myWindow.onload = function(){ 
            var data = JSON.parse(donnees);            
            let table = myWindow.document.querySelector("table");
            let head = Object.keys({"coord-x":"","coord-y":"","date-deb":"","date-dec":"","dete-fin":"","date-ins":"","latitude":"","longitude":"","nbr-ext":"","no-dec":"","no-qr":"","nom-arr":"","nom-qr":""});
            generateTableHead(table, head);
            generateTable(table, data);        
        }                 
            
    })                                     
    .catch((exception) => {
        console.log(exception);
    });
       
  }
  
//   fonctionnalité D1
  function declarer() {
    var nomQuartier = document.getElementById("quartierId");
    var nomArrondi = document.getElementById("arrondiId");
    var adresse = document.getElementById("adressId");
    var date = document.getElementById("dateId");
    var nomPrenom = document.getElementById("nomId");
    var description = document.getElementById("descriptionId");

    var entry = {
        quartier : nomQuartier.value,
        arrondissement : nomArrondi.value,
        adresse : adresse.value,
        date : date.value,
        nomPrenom : nomPrenom.value,
        description : description.value
    }
    fetch(`${window.origin}/api/declaration`, {
        method: 'POST',
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json" 
        })
        
    })
      .then(function (response) {         
         return response.json();         
      })
      .then(function(donnees) {          
        console.log('Request successful', donnees);
        if(donnees.messageErreur){
            document.getElementById('msg').innerHTML = donnees.messageErreur;
        }else{
            document.getElementById('msg').innerHTML ="Les données sont enregistrées et l'identifiant est " + donnees["id"];  
        }
      })
      .catch(function(error) {
        console.log('Request failed', error);
      });
     
  }


function supprimerQuartier() {
    var quartier = document.getElementById("subject").value;    
    fetch(`${window.origin}/api/declaration`, {        
        method: 'DELETE',
        credentials: "include",
        body: JSON.stringify(quartier),
        cache: "no-cache",                
        headers: {
            'Accept': 'application/json',
            'Content-Type' : 'application/json'            
        }             
    })
    .then((response) => {
        if (response.status == 200) {
            document.getElementById('listquartier').innerHTML = "Les données du "+ quartier+" ont été supprimée avec succès."                                
            return response.text();
        }
        else
        {
            throw `error with status ${response.status}`;
        }
    })                   
    .catch((exception) => {
        console.log(exception);
    });
        
    }
    

       
    function creerprofile() {


        setTimeout(function() {
            var messageEffacer= document.getElementById('profileId').innerHTML = "";
            messageEffacer; 
          }, 4000);
        
          
        var nom = document.getElementById("utilisateurId");
        var courriel = document.getElementById("courrielId");
        var liste = document.getElementById("listeId");
        var motPass = document.getElementById("motPassId");
           
        var entry = {
            nom : nom.value,
            courriel : courriel.value,
            liste : liste.value,
            motPass : motPass.value
        }
        fetch(`${window.origin}/api/profile`, {
            method: 'POST',
            credentials: "include",
            body: JSON.stringify(entry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json" 
            })
            
        })
          .then(function (response) {         
             return response.json();         
          })
          .then(function(donnees) {          
            
            if(donnees.messageErreur){
                document.getElementById('profileId').innerHTML = donnees.messageErreur;
            }else{
                document.getElementById('profileId').innerHTML = "Le profil a été créé avec succès.";
                               
            }
          })
          .catch(function(error) {
            console.log('Request failed', error);
          });         
    }    