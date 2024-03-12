function d(n){
    a=0
    b=0
    captal=0
    quanti=10
    while(b<n*2-1){
        if(b<a){
            a=0
        }
        captal=captal+quanti*Math.pow(1.01,a)*0.01
        a=a+1
        b=b+0.5
    }
    return captal
}
anne=2
day = 2*2*2*2*2*2*2*2*2
console.log("res",day,10*Math.pow(1.01,day),(d(day)/(day))*15)