async function render(){
  const res = await fetch('/api/stock/state');
  const arr = await res.json();
  const container = document.getElementById('shelves');
  container.innerHTML = '';
  arr.forEach(s => {
    const el = document.createElement('div');
    el.className = 'shelf ' + (s.status==='EMPTY'?'empty':'occupied');
    el.innerText = s.slot + '\n' + (s.product||'--');
    el.onclick = ()=>{manualToggle(s)};
    container.appendChild(el);
  })
}

async function manualToggle(s){
  const sku = prompt('SKU (入庫の場合)');
  if(s.status==='EMPTY'){
    if(!sku) return;
    const r = await fetch('/api/stock/in/manual', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({slot:s.slot, sku})});
    if(!r.ok){
      const j = await r.json().catch(()=>({error:'unknown'}));
      toast('入庫エラー: '+(j.error||j.code||'unknown'))
    }
  }else{
    const r = await fetch('/api/stock/out/manual', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({slot:s.slot})});
    if(!r.ok){
      const j = await r.json().catch(()=>({error:'unknown'}));
      toast('出庫エラー: '+(j.error||j.code||'unknown'))
    }
  }
  render();
}

document.getElementById('in-auto').addEventListener('click', async ()=>{
  const sku = document.getElementById('sku').value;
  const r = await fetch('/api/stock/in/auto', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({sku})});
  if(!r.ok){ const j = await r.json().catch(()=>({error:'unknown'})); toast('入庫エラー: '+(j.error||j.code||'unknown')); }
  render();
});

document.getElementById('out-auto').addEventListener('click', async ()=>{
  const sku = document.getElementById('sku').value;
  const r = await fetch('/api/stock/out/auto', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({sku})});
  if(!r.ok){ const j = await r.json().catch(()=>({error:'unknown'})); toast('出庫エラー: '+(j.error||j.code||'unknown')); }
  render();
});

setInterval(render, 3000);
render();
