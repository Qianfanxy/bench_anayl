
await figma.setCurrentPageAsync(figma.getNodeById("5:2"));
const ids=["25:309","25:321","25:340","26:341","27:414","27:497","28:468","28:520","29:533","29:554"];
const names=["01_Splash","02_Welcome","03_Name","04_Home","05_Product_Quinoa","06_Basket","07_Checkout_Delivery","08_Checkout_Card","09_Order_Complete","10_Track_Order"];
let out=[];
for(let i=0;i<ids.length;i++){
  const f=figma.getNodeById(ids[i]);
  out.push(names[i]+"="+(f?(f.name+" "+f.width+"x"+f.height+" reactions:"+f.reactions.length):"MISSING"));
}
let reactionCount=0;
for(const p of figma.currentPage.children){ for(const n of p.findAll(()=>true)){ if(n.reactions&&n.reactions.length) reactionCount+=n.reactions.length; } }
const c73=figma.getNodeById("3:21")?"components frame OK":"components frame MISSING";
const m22=figma.getNodeById("2:2")?"media frame OK":"media frame MISSING";
const b42=figma.getNodeById("4:2")?"brief frame OK":"brief frame MISSING";
const f12=figma.getNodeById("1:2")?"foundations OK":"foundations MISSING";
return out.join(" | ")+" || totalReactionNodes:"+reactionCount+" || "+c73+", "+m22+", "+b42+", "+f12;
