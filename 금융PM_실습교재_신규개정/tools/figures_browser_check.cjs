// Read all twenty figures in the actual chapter at desktop and narrow widths.
const path = require('node:path');
module.exports = async function(context, base, check, root) {
  const page = await context.newPage();
  await page.goto(base+'learn.html?unit=0&view=chapter');
  await page.locator('#chapter-title').waitFor();
  await page.evaluate(()=>PMApp.api('/api/stage',{body:JSON.stringify({stage:'S4'})}));
  for(let unit=0;unit<10;unit++) {
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base+`learn.html?unit=${unit}&view=chapter`);
    await page.locator('.chapter-figure').first().waitFor();
    await page.evaluate(()=>document.fonts.ready);
    check(`unit ${unit}: two in-context explanatory figures`,await page.locator('.chapter-figure').count()===2);
    check(`unit ${unit}: reading starts without simulation`,await page.locator('iframe').count()===0);
    const bounds=await page.locator('.figure-desktop svg').evaluateAll(svgs=>svgs.flatMap(svg=>{
      const {width,height}=svg.viewBox.baseVal;
      return [...svg.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x<0||b.y<0||b.x+b.width>width+1||b.y+b.height>height+1}).map(t=>t.textContent);
    }));
    check(`unit ${unit}: SVG text stays in the viewBox`,bounds.length===0);
    for (const fig of await page.locator('.chapter-figure').all()) {
      const id=await fig.getAttribute('data-figure');
      await fig.screenshot({path:path.join(root,'검증',`Figure-${id}.png`)});
    }
    for(const width of [390,320]) {
      await page.setViewportSize({width,height:844});
      check(`unit ${unit}: ${width}px chapter has no horizontal overflow`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
      check(`unit ${unit}: ${width}px diagrams reflow into readable nodes`,await page.locator('.figure-mobile').first().isVisible()&&!await page.locator('.figure-desktop').first().isVisible());
      check(`unit ${unit}: ${width}px diagram body text remains 16px`,await page.locator('.figure-node').evaluateAll(nodes=>nodes.every(n=>parseFloat(getComputedStyle(n).fontSize)>=16)));
    }
    if([0,3,8].includes(unit))await page.locator('.chapter-figure').first().screenshot({path:path.join(root,'검증',`Figure-mobile-u${unit}.png`)});
  }
  await page.close();
};
