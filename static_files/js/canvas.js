const cvs = document.getElementById("pad");
const ctx = cvs.getContext("2d");
ctx.lineCap = "round"; ctx.lineWidth = 4;
let drawing = false;

function pos(ev){ const r = cvs.getBoundingClientRect();
  return [ev.clientX - r.left, ev.clientY - r.top]; }

cvs.addEventListener("pointerdown", ev => {drawing = true;
  ctx.beginPath(); ctx.moveTo(...pos(ev));});
cvs.addEventListener("pointermove", ev => { if(!drawing) return;
  ctx.lineTo(...pos(ev)); ctx.stroke();});
cvs.addEventListener("pointerup",   () => drawing=false);
cvs.addEventListener("pointerleave",() => drawing=false);

document.getElementById("doodleForm").addEventListener("submit", e=>{
  e.target.querySelector("[name=dataurl]").value = cvs.toDataURL("image/png");
/home/gtoscano/projects/django/VulShedula/templates/core/doodles
/home/gtoscano/projects/django/VulShedula/templates/core/doodles/_card.html
/home/gtoscano/projects/django/VulShedula/templates/core/doodles/index.hml
});
