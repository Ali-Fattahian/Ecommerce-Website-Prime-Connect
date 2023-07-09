"use strict";(self.webpackChunkfrontend=self.webpackChunkfrontend||[]).push([[643],{5006:function(e,a,t){t(2791);var n=t(2469),r=t(184);a.Z=function(e){var a=e.variant,t=e.children,l=e.className;return(0,r.jsx)(n.Z,{variant:a,className:"".concat(l),children:t})}},8643:function(e,a,t){t.r(a);var n=t(3433),r=t(9439),l=t(2791),o=t(5006),s=t(5630),i=t(3360),c=t(2677),u=t(9743),d=t(2592),m=t(7689),f=t(9434),p=t(2753),h=t(184);a.default=function(){var e=(0,l.useState)(null),a=(0,r.Z)(e,2),t=a[0],Z=a[1],x=(0,l.useState)(null),g=(0,r.Z)(x,2),y=g[0],b=g[1],j=(0,l.useState)(null),v=(0,r.Z)(j,2),C=v[0],N=v[1],S=(0,l.useState)(""),L=(0,r.Z)(S,2),w=L[0],I=L[1],k=(0,l.useState)(""),P=(0,r.Z)(k,2),z=P[0],D=P[1],G=(0,l.useState)(""),R=(0,r.Z)(G,2),E=R[0],q=R[1],A=(0,l.useState)(""),O=(0,r.Z)(A,2),U=O[0],T=O[1],M=(0,l.useState)(""),V=(0,r.Z)(M,2),B=V[0],H=V[1],F=(0,l.useState)(""),W=(0,r.Z)(F,2),J=W[0],K=W[1],Q=(0,l.useState)(!1),X=(0,r.Z)(Q,2),Y=X[0],$=X[1],_=(0,l.useState)(""),ee=(0,r.Z)(_,2),ae=ee[0],te=ee[1],ne=(0,m.s0)(),re=(0,f.I0)(),le=(0,l.useState)([]),oe=(0,r.Z)(le,2),se=oe[0],ie=oe[1],ce=(0,l.useState)(""),ue=(0,r.Z)(ce,2),de=ue[0],me=ue[1],fe=(0,f.v9)((function(e){return e.user})),pe=(0,f.v9)((function(e){return e.products})),he=fe.userInfo,Ze=pe.loading,xe=pe.error,ge=pe.success,ye=pe.allSubCategories;return(0,l.useEffect)((function(){!1===he.isAdmin&&ne("/login"),0===ye.length&&re((0,p.fV)())}),[ne,he.id,he.isAdmin,re]),(0,h.jsx)("div",{className:"p-4 w-100",style:{maxWidth:"800px",margin:"auto"},children:!xe&&(0,h.jsxs)(s.Z,{onSubmit:function(e){e.preventDefault();var a=(0,n.Z)(new Map(se.map((function(e){return[e.id,e]}))).values()),t=new FormData;t.append("name",w),t.append("brand",z),t.append("description",E),t.append("moreDetails",U),t.append("price",B),t.append("discount",J),t.append("countInStock",ae),t.append("hasDiscount",Y),t.append("subCategory",de),a.forEach((function(e){return t.append("image".concat(e.id),e.image)}));var r=he.token;re((0,p.ry)({formData:t,token:r}))},id:"register-form",className:"p-4 border-lt mt-4",encType:"multipart/form-data",method:"POST",children:[(0,h.jsx)("h1",{className:"font-family-secondary txt--black text-center",style:{fontSize:"3rem"},children:"Create Product"}),(0,h.jsxs)(s.Z.Group,{controlId:"name",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Name"}),(0,h.jsx)(s.Z.Control,{required:!0,autoComplete:"true",type:"text",placeholder:"Enter Name",value:w,onChange:function(e){return I(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"brand",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Brand"}),(0,h.jsx)(s.Z.Control,{required:!0,autoComplete:"true",type:"text",placeholder:"Enter Brand",value:z,onChange:function(e){return D(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"sub-categories",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Sub Category"}),(0,h.jsxs)(s.Z.Select,{required:!0,className:"mb-2",value:de,onChange:function(e){me(e.target.value)},children:[(0,h.jsx)("option",{children:"-----------"}),ye.map((function(e){return(0,h.jsx)("option",{value:e.id,children:e.name},e.id)}))]})]}),(0,h.jsxs)(s.Z.Group,{controlId:"description",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Description"}),(0,h.jsx)(s.Z.Control,{required:!0,maxLength:355,autoComplete:"true",as:"textarea",placeholder:"Description",value:E,onChange:function(e){return q(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"moreDetails",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"More Details"}),(0,h.jsx)(s.Z.Control,{autoComplete:"true",as:"textarea",placeholder:"More Details",value:U,onChange:function(e){return T(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"price",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Price"}),(0,h.jsx)(s.Z.Control,{required:!0,autoComplete:"true",type:"number",placeholder:"Price",value:B,max:"99999",onChange:function(e){return H(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"countInStock",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Products in Stock"}),(0,h.jsx)(s.Z.Control,{required:!0,min:0,autoComplete:"true",type:"number",placeholder:"Products in Stock",value:ae,onChange:function(e){return te(e.target.value)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"discount",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Discount Number"}),(0,h.jsx)(s.Z.Control,{required:!0,min:0,max:99,autoComplete:"true",type:"number",placeholder:"A number between 0 and 99",value:J,onChange:function(e){K(e.target.value),Number(e.target.value)>0?$(!0):0===Number(e.target.value)&&$(!1)}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"image1",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary mb-2",style:{fontSize:"1.5rem"},children:"Add Image 1"}),(0,h.jsx)(s.Z.Control,{type:"file",accept:"image/*",onChange:function(e){ie((function(a){return[].concat((0,n.Z)(a),[{id:1,image:e.target.files[0]}])})),Z(URL.createObjectURL(e.target.files[0]))}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"image2",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary mb-2",style:{fontSize:"1.5rem"},children:"Add Image 2"}),(0,h.jsx)(s.Z.Control,{type:"file",accept:"image/*",onChange:function(e){ie((function(a){return[].concat((0,n.Z)(a),[{id:2,image:e.target.files[0]}])})),b(URL.createObjectURL(e.target.files[0]))}})]}),(0,h.jsxs)(s.Z.Group,{controlId:"image3",children:[(0,h.jsx)(s.Z.Label,{className:"font-family-secondary mb-2",style:{fontSize:"1.5rem"},children:"Add Image 3"}),(0,h.jsx)(s.Z.Control,{type:"file",accept:"image/*",onChange:function(e){ie((function(a){return[].concat((0,n.Z)(a),[{id:3,image:e.target.files[0]}])})),N(URL.createObjectURL(e.target.files[0]))}})]}),(0,h.jsxs)(u.Z,{className:"w-100 gap-4 justify-content-center",children:[t&&(0,h.jsx)(c.Z,{lg:3,xl:3,md:12,sm:12,children:(0,h.jsx)(d.Z,{fluid:!0,alt:"Image 1",src:t,style:{width:"100%"},className:"mt-2"})}),y&&(0,h.jsx)(c.Z,{lg:3,xl:3,md:12,sm:12,children:(0,h.jsx)(d.Z,{fluid:!0,alt:"Image 2",src:y,style:{width:"100%"},className:"mt-2"})}),C&&(0,h.jsx)(c.Z,{lg:3,xl:3,md:12,sm:12,children:(0,h.jsx)(d.Z,{fluid:!0,alt:"Image 3",src:C,style:{width:"100%"},className:"mt-2"})})]}),ge&&(0,h.jsx)(o.Z,{variant:"success",children:"The product was made successfully"}),xe&&(0,h.jsx)(o.Z,{variant:"danger",children:"There was a problem creating the product, Please make sure you filled all the required fields."}),(0,h.jsx)(i.Z,{type:"submit",className:"w-100",style:{color:"var(--bs-secondary)"},variant:"primary",children:Ze?"Loading":"Create"})]})})}},2469:function(e,a,t){var n=t(1413),r=t(5987),l=t(1694),o=t.n(l),s=t(2791),i=t(8580),c=t(9007),u=t(6445),d=t(162),m=t(2709),f=t(473),p=t(7472),h=t(6543),Z=t(184),x=["bsPrefix","show","closeLabel","closeVariant","className","children","variant","onClose","dismissible","transition"],g=(0,p.Z)("h4");g.displayName="DivStyledAsH4";var y=(0,h.Z)("alert-heading",{Component:g}),b=(0,h.Z)("alert-link",{Component:u.Z}),j={variant:"primary",show:!0,transition:m.Z,closeLabel:"Close alert"},v=s.forwardRef((function(e,a){var t=(0,i.Ch)(e,{show:"onClose"}),l=t.bsPrefix,s=t.show,u=t.closeLabel,p=t.closeVariant,h=t.className,g=t.children,y=t.variant,b=t.onClose,j=t.dismissible,v=t.transition,C=(0,r.Z)(t,x),N=(0,d.vE)(l,"alert"),S=(0,c.Z)((function(e){b&&b(!1,e)})),L=!0===v?m.Z:v,w=(0,Z.jsxs)("div",(0,n.Z)((0,n.Z)({role:"alert"},L?void 0:C),{},{ref:a,className:o()(h,N,y&&"".concat(N,"-").concat(y),j&&"".concat(N,"-dismissible")),children:[j&&(0,Z.jsx)(f.Z,{onClick:S,"aria-label":u,variant:p}),g]}));return L?(0,Z.jsx)(L,(0,n.Z)((0,n.Z)({unmountOnExit:!0},C),{},{ref:void 0,in:s,children:w})):s?w:null}));v.displayName="Alert",v.defaultProps=j,a.Z=Object.assign(v,{Link:b,Heading:y})},2592:function(e,a,t){var n=t(1413),r=t(5987),l=t(1694),o=t.n(l),s=t(2791),i=t(2007),c=t.n(i),u=t(162),d=t(184),m=["bsPrefix","className","fluid","rounded","roundedCircle","thumbnail"],f=(c().string,c().bool,c().bool,c().bool,c().bool,s.forwardRef((function(e,a){var t=e.bsPrefix,l=e.className,s=e.fluid,i=e.rounded,c=e.roundedCircle,f=e.thumbnail,p=(0,r.Z)(e,m);return t=(0,u.vE)(t,"img"),(0,d.jsx)("img",(0,n.Z)((0,n.Z)({ref:a},p),{},{className:o()(l,s&&"".concat(t,"-fluid"),i&&"rounded",c&&"rounded-circle",f&&"".concat(t,"-thumbnail"))}))})));f.displayName="Image",f.defaultProps={fluid:!1,rounded:!1,roundedCircle:!1,thumbnail:!1},a.Z=f},9743:function(e,a,t){var n=t(1413),r=t(5987),l=t(1694),o=t.n(l),s=t(2791),i=t(162),c=t(184),u=["bsPrefix","className","as"],d=s.forwardRef((function(e,a){var t=e.bsPrefix,l=e.className,s=e.as,d=void 0===s?"div":s,m=(0,r.Z)(e,u),f=(0,i.vE)(t,"row"),p=(0,i.pi)(),h=(0,i.zG)(),Z="".concat(f,"-cols"),x=[];return p.forEach((function(e){var a,t=m[e];delete m[e],a=null!=t&&"object"===typeof t?t.cols:t;var n=e!==h?"-".concat(e):"";null!=a&&x.push("".concat(Z).concat(n,"-").concat(a))})),(0,c.jsx)(d,(0,n.Z)((0,n.Z)({ref:a},m),{},{className:o().apply(void 0,[l,f].concat(x))}))}));d.displayName="Row",a.Z=d}}]);
//# sourceMappingURL=643.9544d6fd.chunk.js.d8a265b1975d.map