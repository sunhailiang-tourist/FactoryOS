import{f as G,s as V,h as z,i as A,j as n,b as H,d as K,e as O,k as g,l as w,m as I}from"./DefaultPropsProvider-CVNampxs.js";import{c as E,g as F,C as q,a as W,b as Z,s as b,m as L,d as J,T as Q}from"./Typography-nvdT-nkT.js";import{r as _}from"./index-D4fpSGDK.js";function X(r={}){const{themeId:e,defaultTheme:s,defaultClassName:o="MuiBox-root",generateClassName:c}=r,d=G("div",{shouldForwardProp:a=>a!=="theme"&&a!=="sx"&&a!=="as"})(V);return _.forwardRef(function(h,l){const i=z(s),{className:u,component:x="div",...m}=A(h);return n.jsx(d,{as:x,ref:l,className:E(u,c?c(o):o),theme:e&&i[e]||i,...m})})}const Y=F("MuiBox",["root"]),ee=K(),re=X({themeId:H,defaultTheme:ee,defaultClassName:Y.root,generateClassName:q.generate});function se(r){return W("MuiCircularProgress",r)}F("MuiCircularProgress",["root","determinate","indeterminate","colorPrimary","colorSecondary","svg","circle","circleDeterminate","circleIndeterminate","circleDisableShrink"]);const t=44,C=I`
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
`,k=I`
  0% {
    stroke-dasharray: 1px, 200px;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 100px, 200px;
    stroke-dashoffset: -15px;
  }

  100% {
    stroke-dasharray: 1px, 200px;
    stroke-dashoffset: -126px;
  }
`,ae=typeof C!="string"?w`
        animation: ${C} 1.4s linear infinite;
      `:null,te=typeof k!="string"?w`
        animation: ${k} 1.4s ease-in-out infinite;
      `:null,oe=r=>{const{classes:e,variant:s,color:o,disableShrink:c}=r,d={root:["root",s,`color${g(o)}`],svg:["svg"],circle:["circle",`circle${g(s)}`,c&&"circleDisableShrink"]};return Z(d,se,e)},ie=b("span",{name:"MuiCircularProgress",slot:"Root",overridesResolver:(r,e)=>{const{ownerState:s}=r;return[e.root,e[s.variant],e[`color${g(s.color)}`]]}})(L(({theme:r})=>({display:"inline-block",variants:[{props:{variant:"determinate"},style:{transition:r.transitions.create("transform")}},{props:{variant:"indeterminate"},style:ae||{animation:`${C} 1.4s linear infinite`}},...Object.entries(r.palette).filter(J()).map(([e])=>({props:{color:e},style:{color:(r.vars||r).palette[e].main}}))]}))),ne=b("svg",{name:"MuiCircularProgress",slot:"Svg",overridesResolver:(r,e)=>e.svg})({display:"block"}),ce=b("circle",{name:"MuiCircularProgress",slot:"Circle",overridesResolver:(r,e)=>{const{ownerState:s}=r;return[e.circle,e[`circle${g(s.variant)}`],s.disableShrink&&e.circleDisableShrink]}})(L(({theme:r})=>({stroke:"currentColor",variants:[{props:{variant:"determinate"},style:{transition:r.transitions.create("stroke-dashoffset")}},{props:{variant:"indeterminate"},style:{strokeDasharray:"80px, 200px",strokeDashoffset:0}},{props:({ownerState:e})=>e.variant==="indeterminate"&&!e.disableShrink,style:te||{animation:`${k} 1.4s ease-in-out infinite`}}]}))),le=_.forwardRef(function(e,s){const o=O({props:e,name:"MuiCircularProgress"}),{className:c,color:d="primary",disableShrink:P=!1,size:a=40,style:h,thickness:l=3.6,value:i=0,variant:u="indeterminate",...x}=o,m={...o,color:d,disableShrink:P,size:a,thickness:l,value:i,variant:u},y=oe(m),v={},S={},D={};if(u==="determinate"){const $=2*Math.PI*((t-l)/2);v.strokeDasharray=$.toFixed(3),D["aria-valuenow"]=Math.round(i),v.strokeDashoffset=`${((100-i)/100*$).toFixed(3)}px`,S.transform="rotate(-90deg)"}return n.jsx(ie,{className:E(y.root,c),style:{width:a,height:a,...S,...h},ownerState:m,ref:s,role:"progressbar",...D,...x,children:n.jsx(ne,{className:y.svg,ownerState:m,viewBox:`${t/2} ${t/2} ${t} ${t}`,children:n.jsx(ce,{className:y.circle,style:v,ownerState:m,cx:t,cy:t,r:(t-l)/2,fill:"none",strokeWidth:l})})})});function U({label:r="加载中"}){return n.jsxs(re,{display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center",minHeight:"40vh",gap:1,children:[n.jsx(le,{"aria-label":r}),n.jsx(Q,{variant:"body2",color:"text.secondary",children:r})]})}U.__docgenInfo={description:"",methods:[],displayName:"PageLoading",props:{label:{required:!1,tsType:{name:"string"},description:"",defaultValue:{value:'"加载中"',computed:!1}}}};const pe={title:"Global/Feedback/PageLoading",component:U,tags:["autodocs"]},p={},f={args:{label:"正在加载 Studio…"}};var N,j,M;p.parameters={...p.parameters,docs:{...(N=p.parameters)==null?void 0:N.docs,source:{originalSource:"{}",...(M=(j=p.parameters)==null?void 0:j.docs)==null?void 0:M.source}}};var R,B,T;f.parameters={...f.parameters,docs:{...(R=f.parameters)==null?void 0:R.docs,source:{originalSource:`{
  args: {
    label: "正在加载 Studio…"
  }
}`,...(T=(B=f.parameters)==null?void 0:B.docs)==null?void 0:T.source}}};const fe=["Default","CustomLabel"];export{f as CustomLabel,p as Default,fe as __namedExportsOrder,pe as default};
