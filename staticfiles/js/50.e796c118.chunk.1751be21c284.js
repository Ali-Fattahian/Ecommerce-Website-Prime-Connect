"use strict";(self.webpackChunkfrontend=self.webpackChunkfrontend||[]).push([[50],{5524:function(e,a,n){n(2791);var r=n(7022),s=n(9743),t=n(2677),o=n(184);a.Z=function(e){var a=e.children,n=e.className;return(0,o.jsx)(r.Z,{children:(0,o.jsx)(s.Z,{className:"justify-content-md-center ".concat(n),children:(0,o.jsx)(t.Z,{xs:12,md:6,children:a})})})}},5006:function(e,a,n){n(2791);var r=n(2469),s=n(184);a.Z=function(e){var a=e.variant,n=e.children,t=e.className;return(0,s.jsx)(r.Z,{variant:a,className:"".concat(t),children:n})}},50:function(e,a,n){n.r(a);var r=n(9439),s=n(2791),t=n(7689),o=n(1087),l=n(9434),i=n(5630),c=n(3360),d=n(9743),u=n(2677),f=n(8152),m=n(5006),Z=n(5802),h=n(5524),p=n(184);a.default=function(){var e=(0,s.useState)(""),a=(0,r.Z)(e,2),n=a[0],v=a[1],x=(0,s.useState)(""),y=(0,r.Z)(x,2),j=y[0],N=y[1],b=(0,s.useState)(""),C=(0,r.Z)(b,2),w=C[0],g=C[1],S=(0,s.useState)(""),P=(0,r.Z)(S,2),k=P[0],z=P[1],E=(0,s.useState)(""),L=(0,r.Z)(E,2),I=L[0],R=L[1],G=window.location.search?window.location.search.split("=")[1]:"",q=(0,t.s0)(),A=(0,l.I0)(),H=(0,l.v9)((function(e){return e.user})),D=H.error,F=H.loading;return(0,p.jsxs)(h.Z,{className:"pt-3",children:[I&&(0,p.jsx)(m.Z,{variant:"danger",children:I}),D&&(0,p.jsx)(m.Z,{variant:"danger",children:D}),F&&(0,p.jsx)(f.Z,{}),(0,p.jsxs)(i.Z,{onSubmit:function(e){e.preventDefault(),w!==k?R("Passwords do not match"):(A((0,Z.z2)({fullname:j,email:n,password:w})),q("/"))},id:"register-form",className:"p-4 border-lt mt-4",children:[(0,p.jsx)("h1",{className:"font-family-secondary txt--black text-center",style:{fontSize:"3rem"},children:"Register"}),(0,p.jsxs)(i.Z.Group,{controlId:"name",children:[(0,p.jsx)(i.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Full Name"}),(0,p.jsx)(i.Z.Control,{required:!0,autoComplete:"true",type:"text",placeholder:"Enter Full Name",value:j,onChange:function(e){return N(e.target.value)}})]}),(0,p.jsxs)(i.Z.Group,{controlId:"email",children:[(0,p.jsx)(i.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Email Address"}),(0,p.jsx)(i.Z.Control,{required:!0,autoComplete:"true",type:"email",placeholder:"Enter Email",value:n,onChange:function(e){return v(e.target.value)}})]}),(0,p.jsxs)(i.Z.Group,{controlId:"password",children:[(0,p.jsx)(i.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Password"}),(0,p.jsx)(i.Z.Control,{required:!0,autoComplete:"true",type:"password",placeholder:"Password",value:w,onChange:function(e){return g(e.target.value)}})]}),(0,p.jsxs)(i.Z.Group,{controlId:"passwordConfirm",children:[(0,p.jsx)(i.Z.Label,{className:"font-family-secondary",style:{fontSize:"1.5rem"},children:"Confirm Password"}),(0,p.jsx)(i.Z.Control,{required:!0,autoComplete:"true",type:"password",placeholder:"Confirm Password",value:k,onChange:function(e){return z(e.target.value)}})]}),(0,p.jsx)("p",{style:{fontSize:"1.2rem"},className:"txt--gray font-family-secondary d-inline-block",children:"Have an Account?"}),(0,p.jsx)(o.Link,{to:G?"/login?redirect=".concat(G):"/login",className:"font-family-secondary px-2",style:{fontSize:"1.2rem"},children:"Sign In"}),(0,p.jsx)(c.Z,{type:"submit",className:"w-100",style:{backgroundColor:"var(--bs-primary)",color:"var(--bs-secondary)"},children:"Register"})]}),(0,p.jsx)(d.Z,{className:"py-3",children:(0,p.jsx)(u.Z,{})})]})}},2469:function(e,a,n){var r=n(1413),s=n(5987),t=n(1694),o=n.n(t),l=n(2791),i=n(8580),c=n(9007),d=n(6445),u=n(162),f=n(2709),m=n(473),Z=n(7472),h=n(6543),p=n(184),v=["bsPrefix","show","closeLabel","closeVariant","className","children","variant","onClose","dismissible","transition"],x=(0,Z.Z)("h4");x.displayName="DivStyledAsH4";var y=(0,h.Z)("alert-heading",{Component:x}),j=(0,h.Z)("alert-link",{Component:d.Z}),N={variant:"primary",show:!0,transition:f.Z,closeLabel:"Close alert"},b=l.forwardRef((function(e,a){var n=(0,i.Ch)(e,{show:"onClose"}),t=n.bsPrefix,l=n.show,d=n.closeLabel,Z=n.closeVariant,h=n.className,x=n.children,y=n.variant,j=n.onClose,N=n.dismissible,b=n.transition,C=(0,s.Z)(n,v),w=(0,u.vE)(t,"alert"),g=(0,c.Z)((function(e){j&&j(!1,e)})),S=!0===b?f.Z:b,P=(0,p.jsxs)("div",(0,r.Z)((0,r.Z)({role:"alert"},S?void 0:C),{},{ref:a,className:o()(h,w,y&&"".concat(w,"-").concat(y),N&&"".concat(w,"-dismissible")),children:[N&&(0,p.jsx)(m.Z,{onClick:g,"aria-label":d,variant:Z}),x]}));return S?(0,p.jsx)(S,(0,r.Z)((0,r.Z)({unmountOnExit:!0},C),{},{ref:void 0,in:l,children:P})):l?P:null}));b.displayName="Alert",b.defaultProps=N,a.Z=Object.assign(b,{Link:j,Heading:y})},7022:function(e,a,n){var r=n(1413),s=n(5987),t=n(1694),o=n.n(t),l=n(2791),i=n(162),c=n(184),d=["bsPrefix","fluid","as","className"],u=l.forwardRef((function(e,a){var n=e.bsPrefix,t=e.fluid,l=e.as,u=void 0===l?"div":l,f=e.className,m=(0,s.Z)(e,d),Z=(0,i.vE)(n,"container"),h="string"===typeof t?"-".concat(t):"-fluid";return(0,c.jsx)(u,(0,r.Z)((0,r.Z)({ref:a},m),{},{className:o()(f,t?"".concat(Z).concat(h):Z)}))}));u.displayName="Container",u.defaultProps={fluid:!1},a.Z=u},9743:function(e,a,n){var r=n(1413),s=n(5987),t=n(1694),o=n.n(t),l=n(2791),i=n(162),c=n(184),d=["bsPrefix","className","as"],u=l.forwardRef((function(e,a){var n=e.bsPrefix,t=e.className,l=e.as,u=void 0===l?"div":l,f=(0,s.Z)(e,d),m=(0,i.vE)(n,"row"),Z=(0,i.pi)(),h=(0,i.zG)(),p="".concat(m,"-cols"),v=[];return Z.forEach((function(e){var a,n=f[e];delete f[e],a=null!=n&&"object"===typeof n?n.cols:n;var r=e!==h?"-".concat(e):"";null!=a&&v.push("".concat(p).concat(r,"-").concat(a))})),(0,c.jsx)(u,(0,r.Z)((0,r.Z)({ref:a},f),{},{className:o().apply(void 0,[t,m].concat(v))}))}));u.displayName="Row",a.Z=u}}]);
//# sourceMappingURL=50.e796c118.chunk.js.29e3917820c5.map