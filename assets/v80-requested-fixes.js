
(()=>{
  // Reviews page: exactly the same horizontal control behavior as the home page.
  document.querySelectorAll('.homeVibeReviews').forEach(section=>{
    const track=section.querySelector('.compactReviewTrack'); const b=section.querySelectorAll('.compactReviewControls button');
    if(track&&b.length){b[0].onclick=()=>track.scrollBy({left:-track.clientWidth*.72,behavior:'smooth'});b[1].onclick=()=>track.scrollBy({left:track.clientWidth*.72,behavior:'smooth'});}
  });
  // Worksheet actions.
  const form=document.querySelector('#preapprovalForm');
  if(form){
    document.querySelector('[data-worksheet-clear]')?.addEventListener('click',()=>form.reset());
    document.querySelector('[data-worksheet-print]')?.addEventListener('click',()=>window.print());
    document.querySelector('[data-worksheet-download]')?.addEventListener('click',()=>{
      const fields=[...form.elements].filter(el=>el.name).map(el=>[el.name,(el.value||'').trim()]);
      const safe=s=>String(s).replace(/\\/g,'\\\\').replace(/\(/g,'\\(').replace(/\)/g,'\\)').replace(/[^\x20-\x7E]/g,' ');
      let y=744; const rows=[];
      rows.push('BT /F1 18 Tf 72 760 Td (Pre Approval Planning Worksheet) Tj ET');
      rows.push('BT /F1 9 Tf 72 742 Td (Sun and Sage - private planning summary) Tj ET');
      y=716;
      fields.forEach(([k,v])=>{ if(y<70)return; rows.push(`BT /F1 9 Tf 72 ${y} Td (${safe(k)}:) Tj ET`); rows.push(`BT /F1 10 Tf 230 ${y} Td (${safe(v||' ')}) Tj ET`); y-=22; });
      const stream=rows.join('\\n');
      const objs=[]; const add=o=>{objs.push(o);return objs.length};
      const catalog=add('<< /Type /Catalog /Pages 2 0 R >>');
      add('<< /Type /Pages /Kids [3 0 R] /Count 1 >>');
      add('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>');
      add(`<< /Length ${stream.length} >>\\nstream\\n${stream}\\nendstream`);
      add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>');
      let pdf='%PDF-1.4\\n', offsets=[0];
      objs.forEach((o,i)=>{offsets.push(pdf.length);pdf+=`${i+1} 0 obj\\n${o}\\nendobj\\n`;});
      const xref=pdf.length; pdf+=`xref\\n0 ${objs.length+1}\\n0000000000 65535 f \\n`; offsets.slice(1).forEach(o=>pdf+=String(o).padStart(10,'0')+' 00000 n \\n');
      pdf+=`trailer << /Size ${objs.length+1} /Root 1 0 R >>\\nstartxref\\n${xref}\\n%%EOF`;
      const blob=new Blob([pdf],{type:'application/pdf'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='Sun-and-Sage-Pre-Approval-Worksheet.pdf'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000);
    });
  }
})();
