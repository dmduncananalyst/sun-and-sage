from pathlib import Path

block = '''/* Framed editorial previews: natural rows, balanced excerpts, complete titles.
   Keep this scoped to the photo/copy/action component, not other card types.
   --ss22-sage and --ss22-paper are the existing direction-v22 brand tokens. */
html body.ss18 main#main#main#main#main .loanHubGrid:has(> .loanHubItem > .final-static-answer) {
 grid-auto-rows:auto!important; align-items:stretch!important;
}
@media(min-width:601px) and (max-width:950px) {
 html body.ss18 main#main#main#main#main .loanHubGrid:has(> .loanHubItem > .final-static-answer) {
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
 }
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem:has(> .final-static-answer) {
 height:auto!important; min-height:0!important; max-height:none!important;
 align-self:stretch!important; box-sizing:border-box!important;
 border:4px solid var(--ss22-sage, #48533e)!important;
 border-radius:0!important; box-shadow:none!important;
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem > .final-static-answer {
 display:flex!important; flex-direction:column!important; flex:0 0 auto!important;
 height:auto!important; min-height:0!important; max-height:none!important;
 justify-content:flex-start!important; gap:0!important;
 padding:18px 20px!important;
 border-top:1px solid var(--ss22-sage, #48533e)!important;
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem > .final-static-answer > h2 {
 height:auto!important; min-height:0!important; max-height:none!important;
 display:block!important; overflow:visible!important;
 -webkit-line-clamp:unset!important; line-clamp:unset!important;
}
/* Clamp the whole excerpt, including any existing supplementary mobile copy.
   Leave all text in the document and never constrain the article itself. */
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem > .final-static-answer > .final-static-answer-copy {
 display:-webkit-box!important; -webkit-box-orient:vertical!important;
 -webkit-line-clamp:4!important; line-clamp:4!important; overflow:hidden!important;
 height:auto!important; min-height:0!important; max-height:none!important; flex:0 0 auto!important;
 border-top:1px solid var(--ss22-line, #cdd1c3)!important;
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem > .final-static-answer > .final-static-answer-copy p {
 display:block!important; height:auto!important; min-height:0!important; max-height:none!important;
 -webkit-line-clamp:unset!important; line-clamp:unset!important; overflow:visible!important;
}
/* Supplementary mobile summaries remain hidden on desktop. */
@media(min-width:821px) {
 html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem > .final-static-answer > .final-static-answer-copy p.blog-mobile-summary {display:none!important;}
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem:has(> .final-static-answer) > .loanLearn {
 margin-top:auto!important; flex:0 0 auto!important;
 border-top:1px solid var(--ss22-sage, #48533e)!important;
 background:var(--ss22-paper, #f8f7f3)!important;
 box-shadow:inset 0 -3px 0 var(--ss22-line, #cdd1c3)!important;
}
html body.ss18 main#main#main#main#main .loanHubGrid > .loanHubItem:has(> .final-static-answer) > .loanLearn a:focus-visible {
 outline:2px solid var(--ss22-sage, #48533e)!important; outline-offset:4px!important;
}

'''

block = block.replace('.loanHubGrid:has(> .loanHubItem > .final-static-answer)', '.loanHubGrid:has(> .loanHubItem > .ss18-card-photo):has(> .loanHubItem > .loanLearn)')
block = block.replace('.loanHubGrid > .loanHubItem', '.loanHubGrid > .loanHubItem:has(> .ss18-card-photo):has(> .loanLearn)')

for name in ['75e3427875dcf211', '295473f8529b44f9', 'ad2a85f2e8cb67b7']:
    path = Path('assets/performance-css') / (name + '.css')
    source = (Path('article-card-audit/v2') / (name + '-before.css')).read_bytes()
    newline = b'\r\n' if b'\r\n' in source else b'\n'
    path.write_bytes(source + newline + block.replace('\n', newline.decode()).encode())
