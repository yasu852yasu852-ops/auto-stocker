async function loadQueue(){
  const res = await fetch('/api/queue/');
  const arr = await res.json();
  console.log(arr);
}
setInterval(loadQueue,5000);
loadQueue();
