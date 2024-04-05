function actualiserpris(prix){
    var prixElement = document.getElementById("prix");
    if(prixElement) {
        prixElement.innerText = prix;
    }
    Array.from(document.getElementsByClassName("benfpourcentage")).forEach((element)=>{
        var orderid = element.getAttribute("orderid");
        var QactifElement = document.querySelector("." + MONEY_ECHANGE + "[orderid='"+orderid+"']");
        var QpricipalElement = document.querySelector("." + MONEY_PRINCIPAL + "[orderid='"+orderid+"']");
        var dateElement = document.querySelector("." + DATE + "[orderid='"+orderid+"']");

        if(QactifElement && QpricipalElement && dateElement) {
            var Qactif = QactifElement.innerText;
            var Qpricipal = parseFloat(QpricipalElement.innerText);
            var date = dateElement.innerText;

            var prixbuy = Qpricipal/Qactif;
            var newprix = prixbuy*(1+0.001)*(1+0.001)*Math.pow(1+0.06/(365*24*60*60),(new Date().getTime()-new Date(date).getTime())/1000);

            var newprixElement = document.querySelector(".newprix[orderid='"+orderid+"']");
            var prixbuyElement = document.querySelector(".prixbuy[orderid='"+orderid+"']");
            var benefElement = document.querySelector(".benef[orderid='"+orderid+"']");
            if(newprixElement && prixbuyElement && benefElement) {
                newprixElement.innerText = newprix;
                prixbuyElement.innerText = prixbuy;
                benefElement.innerText = ((prix-newprix)*Qactif)+" " + MONEY_PRINCIPAL;
                element.innerText = (Qpricipal+((prix-newprix)*Qactif))/Qpricipal-1;
                if(element.innerText<=0){
                    document.getElementById(orderid).style.backgroundColor = 'red';
                    document.getElementById(orderid).style.color = 'white'
                }else if(element.innerText<=0.01){
                    document.getElementById(orderid).style.backgroundColor = 'yellow'   
                }else{
                    document.getElementById(orderid).style.backgroundColor = '#00FF00';
                }
            }
        }
    })
}

socket.on("prix",(prix)=>{
    actualiserpris(prix);
});

socket.on("buytime",(time)=>{
    var buytimeElement = document.getElementById("buytime");
    if(buytimeElement) {
        buytimeElement.innerText = time;
    }
});

socket.on("sellprix",(time)=>{
    var sellprixElement = document.getElementById("sellprix");
    if(sellprixElement) {
        sellprixElement.innerText = time;
    }
});

socket.on("del",(id)=>{
    var toRemoveElement = document.getElementById(id);
    if(toRemoveElement) {
        toRemoveElement.remove();
    }
});

socket.on("add",()=>{
    // Implementation for "add" event
});

var initialPrixElement = document.getElementById("prix");
if(initialPrixElement) {
    actualiserpris(initialPrixElement.innerText);
}