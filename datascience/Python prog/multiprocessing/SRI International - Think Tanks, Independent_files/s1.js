try {
   var d = top.document; 
  function crsspxl(z) {
           if(d.body == null || typeof d.body == 'undefined'){
               if(z < 2500){
                   var rec = function() { crsspxl(z * 2); };
                   setTimeout(rec, z);
               }
           }
           else {
               var l = 'http://tag.crsspxl.com/s2.html?d=1005',i,j;
               try {
                   var e = (top.document) ? top.document.referrer : false;
                   var a, f, q, r;
                   if (e) {
                       a = e.split('?q=');
                       a = a.length < 2 ? a[0].split('&q=') : a;
                       a = a.length < 2 ? a[0].split('?p=') : a;
                       f = a.length > 1 ? a[1].split('&') : '';
                       q = f.length >= 1 ? f[0] : '';
                       r = e.split('http://');
                       r = r.length > 1 ? r[1].split('/') : r[0].split('/');
                       r = r[0];
                       if (q && r) {
                           l += "&q=" + q + "&r=" + r;
                       }
                   }
               } catch(er) {
           }
           var t = encodeURIComponent(d.title);
           l += "&t=" + t;
           var u = encodeURIComponent(d.URL);
           l += "&u=" + u;
           try {
               var c = d.getElementsByTagName('META');
               var m = '';
               for (var i=0;i<c.length;i++) {
                   if(c[i].name.toLowerCase() == 'description' || c[i].name.toLowerCase() == 'keywords'){
                       m += (c[i].content + " " || ''); 
                   }
               }
               l += "&m=" + encodeURIComponent(m);
           } catch(er) {
           }
           try {
               var s = d.querySelectorAll("h3");
               var b = '';
               for (j in s) {
                   b += (s[j].innerText || s[j].textContent ? (s[j].innerText ? s[j].innerText.substring(0,400) : s[j].textContent.substring(0,400)) : '');
               }
               b = b.replace(/[\t\r\n]/g, "");
               b = encodeURIComponent(b);
               l += "&b=" + b;
           } catch(er) {
           }
           try {
               var g=d.getElementById('crsspxl_494810001');
               if(typeof(g)!='undefined' && g!=null){
                   g.setAttribute('src', l);
               }
               else{
                   g=d.createElement('IFRAME');
                   g.width=1;
                   g.height=1;
                   g.frameBorder=0;
                   g.border=0;
                   g.marginwidth=0;
                   g.marginheight=0;
                   g.setAttribute('width', '1');
                   g.setAttribute('height', '1');
                   g.setAttribute('style', 'visibility:hidden;position:absolute;border:medium none');
                   g.setAttribute('src', l);
                   d.body.appendChild(g);
               }
           }catch(er){
       }
   }
}

try {
   crsspxl(100);
} catch(er) {
}
} catch(er) {
}
