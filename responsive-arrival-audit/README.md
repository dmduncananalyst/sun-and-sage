# Responsive arrival fix

The responsive header previously depended on deferred navigation-v22.js to set is-compact/is-tablet and place the mobile controls. Until that initialization, iPad and phone could paint the desktop header/menu.

Two small synchronous initializers now establish the existing responsive classes while parsing the header, then place the phone controls and set the header-bottom measurement before parsing the page content. Both initializers return without changes on desktop. Existing navigation behavior, styling, links, videos and content remain intact.

Applied consistently to all 352 live pages. Static preservation checks confirmed no content changes beyond the shared navigation styling reference and these initializers.

Browser verification deliberately delays the main navigation script by two seconds and compares visible menu font sizes and geometry before and after initialization on Home, Contact and Interior Design at 390, 768, 820, 834, 1024 and 1180px. Desktop settled typography is checked against its saved baseline at 1440px. A subpixel position tolerance below 0.5px accounts for browser rounding; menu sizes and typography remain identical.

See review.html for arrival/ready screenshots and results.json for individual checks. No commit, push or publication.
