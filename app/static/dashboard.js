let chart, series;
async function loadMarket(){
 const symbol=document.getElementById('symbol').value;
 document.getElementById('tsymbol').value=symbol;
 const r=await fetch('/api/market/'+symbol); const d=await r.json();
 document.getElementById('quote').textContent=symbol+'  '+Number(d.price).toFixed(symbol==='XAUUSD'?2:5);
 if(!chart){chart=LightweightCharts.createChart(document.getElementById('chart'),{layout:{background:{color:'#0d141f'},textColor:'#b9c6d8'},grid:{vertLines:{color:'#182332'},horzLines:{color:'#182332'}},width:document.getElementById('chart').clientWidth,height:450});series=chart.addCandlestickSeries();}
 series.setData(d.candles); chart.timeScale().fitContent();
}
document.getElementById('symbol').addEventListener('change',loadMarket);
document.getElementById('trade').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.target);const d=Object.fromEntries(f);d.entry=Number(d.entry);d.quantity=Number(d.quantity);for(const k of ['stop_loss','take_profit']) d[k]=d[k]?Number(d[k]):null;const r=await fetch('/api/trades',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});if(r.ok) location.reload();else alert('Could not save trade');});
loadMarket();
