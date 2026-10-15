from pathlib import Path
import re
p=Path('assets/navigation-v22.js');s=p.read_text(encoding='utf-8-sig').replace('ss22-','dd-').replace('dd-compact-nav','is-compact')
s=s.replace("const items=[...nav.children]", "const contacts=header.querySelector('.dd-contact-strip'),tools=header.querySelector('.dd-header-tools');tools.append(toggle);\nconst items=[...nav.children]")
s=re.sub(r"const back=document.createElement\('button'\);.*?nav.prepend\(back\);\n",'',s)
s=re.sub(r"back.addEventListener\('click',.*?\nfunction bind",'function bind',s,flags=re.S)
s=s.replace("String(compact&&flyouts.includes(g))", "'false'")
s=s.replace("nav.classList.remove('submenu-is-open');",'')
s=s.replace("if(compact&&primary.includes(g)){nav.classList.add('submenu-is-open');nav.scrollTop=0;}else place(g);", "if(!(compact&&primary.includes(g)))place(g);")
s=s.replace('--ss-dropdown-', '--dd-panel-').replace('--ss-nav-top','--dd-header-bottom')
# Variables in the previous controller retained their old names despite class isolation.
s=s.replace('--dd-dropdown-','--dd-panel-').replace('--dd-nav-top','--dd-header-bottom')
s=s.replace("function position(){document.documentElement.style.setProperty('--dd-header-bottom',Math.max(0,header.getBoundingClientRect().bottom)+'px');}", """function position(){const root=document.documentElement,gutter=parseFloat(getComputedStyle(header).paddingLeft),width=Math.min(760,root.clientWidth-2*gutter);root.style.setProperty('--dd-header-bottom',Math.max(0,header.getBoundingClientRect().bottom)+'px');root.style.setProperty('--dd-menu-width',width+'px');root.style.setProperty('--dd-menu-left',Math.max(gutter,(root.clientWidth-width)/2)+'px');}""")
start=s.index('function fits()');end=s.index("header.addEventListener('pointerdown'",start)
s=s[:start]+"""// Fit the utility composition and the navigation, with space beyond their text widths.
function fits(){const r=nav.getBoundingClientRect(),rs=items.map(e=>(e.matches('a')?e:trigger(e)).getBoundingClientRect()),zones=[header.querySelector('.dd-brand'),header.querySelector('.dd-rise'),contacts,tools].map(e=>e.getBoundingClientRect());return nav.scrollWidth<=nav.clientWidth+1&&rs.every(a=>a.left>=r.left+24&&a.right<=r.right-24&&Math.abs(a.top-rs[0].top)<2)&&zones.every((z,i)=>z.left>=r.left-1&&z.right<=r.right+1&&(!i||z.left-zones[i-1].right>=27));}
function layout(){header.classList.remove('is-compact');if(contacts.parentElement!==header)header.insertBefore(contacts,nav);const next=innerWidth<1280||!fits();if(next!==compact)closeAll();compact=next;header.classList.toggle('is-compact',compact);if(compact)nav.append(contacts);flyouts.forEach(g=>{if(compact){trigger(g).removeAttribute('aria-expanded');trigger(g).removeAttribute('aria-haspopup');}else{trigger(g).setAttribute('aria-expanded',String(g.classList.contains('is-open')));trigger(g).setAttribute('aria-haspopup','true');}});position();groups.filter(g=>g.classList.contains('is-open')).forEach(place);}
// Keep parent destinations explicit in inline menus, and avoid a second nested accordion.
primary.forEach(g=>{const a=trigger(g),content=g.querySelector('.dd-panel-content');if(![...content.children].some(c=>c.matches('a')&&c.getAttribute('href')===a.getAttribute('href'))){const overview=a.cloneNode(true);overview.className='dd-parent-link';overview.removeAttribute('aria-haspopup');overview.removeAttribute('aria-expanded');content.prepend(overview);}});
const program=nav.querySelector('a[href$="first-time-homebuyer-programs.html"]');if(program){const link=program.cloneNode(true);link.className='dd-mobile-program';nav.querySelector('.dd-buyers>.dd-panel>.dd-panel-content').append(link);}
"""+s[end:]
s=s.replace("if(compact&&fly)return;if(a.matches('button'))", "if(compact&&fly)return;if(compact&&primary.includes(g)){e.preventDefault();g.classList.contains('is-open')?close(g):open();return;}if(a.matches('button'))")
s=s.replace("'.dd-panel a,#dd-navigation>a'", "'.dd-panel a,#dd-navigation>a,.dd-contact-strip a'")
p.write_text(s,encoding='utf-8')
p=Path('assets/v46-mobile-menu.js');s=p.read_text(encoding='utf-8-sig').replace('ss22-','dd-');p.write_text(s,encoding='utf-8')
p=Path('assets/responsive-navigation.css');s=p.read_text(encoding='utf-8-sig');s=s.replace('#dd-header .dd-mobile-program{display:none;}', '#dd-header .dd-mobile-program,#dd-header .dd-parent-link{display:none;}');s=s.replace('#dd-header.is-compact #dd-navigation .dd-mobile-program{display:flex;}', '#dd-header.is-compact #dd-navigation :is(.dd-mobile-program,.dd-parent-link){display:flex;}');p.write_text(s,encoding='utf-8');print('Updated shared header controller, scroll lock, and isolated styles.')
