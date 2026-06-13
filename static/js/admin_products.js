async function loadProducts(){
  const r = await fetch('/api/products/');
  const arr = await r.json();
  const el = document.getElementById('prod-list');
  el.innerHTML = '';
  arr.forEach(p=>{
    const row = document.createElement('div');
    row.innerText = p.sku + ' — ' + p.name;
    el.appendChild(row);
  })
}

async function addProduct(){
  const sku = document.getElementById('p-sku').value;
  const name = document.getElementById('p-name').value;
  const r = await fetch('/api/products/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({sku,name})});
  if(!r.ok){ alert('作成エラー'); }
  else{ document.getElementById('p-sku').value=''; document.getElementById('p-name').value=''; loadProducts(); }
}

window.addEventListener('load', ()=>{ loadProducts(); document.getElementById('p-add').addEventListener('click', addProduct); });
