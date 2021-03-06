let h=0;
let s=0;
let v=0;

function init(){
    setSource(1);
    if(pNodeC > 0){
        nLedC = nLedC/4;
        setGroup(0, [0, 7, 8, 15]);
        setGroup(1, [1, 6, 9, 14]);
        setGroup(2, [2, 5, 10, 13]);
        setGroup(3, [3, 4, 11, 12]);
    }
}

function update(delta){
    if(vol === 0 || freq === 0 || vol < lVol){
        if(v > 0.05){ v-=0.05; }
        else{ v=0; }
    } else {
        h=map(freq,0,maxF,250,0);
        s=1;
        v=map(vol,0,100,0,1);
    }

    if(pNodeC === 0) {
        let newColor=xhsv(h,s,v);
        for(let i=nLedC-1; i>=0;i--){
            setLed(i, newColor);
        }
    } else {
        for(let i=nLedC-1; i>0;i--){
            setLed(i, getLed(i-1));
        }
        setLed(0, xhsv(h,s,v));
    }    
}

function getName() { return "Desktop"; }