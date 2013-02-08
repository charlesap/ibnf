import sys
from binascii import *

fi = file(sys.argv[1]).read()
semantics = file(sys.argv[2]).read()
fo = open(sys.argv[3], "w+")

h={}; registers={}; context={}; mseq=0; dseq=1; T=True; F=False

def n2z( a ):
  return ( '0' if a=='' else a )

def be2le( a ):
  return a[6:8]+a[4:6]+a[2:4]+a[0:2]

def mark( p, s, t ):
  ( v, m, ss, l, c, a ) = t
  if t[1]:  x = p +"-" + str(s);  h[x]=(v,m,l,a); return t
  else:
    if not t[0]:  x = p +"-" + str(s);  h[x]=(v,m,l,a); return t
  return t

def been(p, s):
 if h.has_key( p +"-" + str(s) ): return h[p +"-" + str(s)][1]
 else:  return False

def was(c,p,s): (v,m,l,a) = h[p+"-"+str(s)]; return (v,m,s,l,c,a) 

def cm( ch, s, c ):
  if s < len(fi):
    if fi[s] == ch:    return ( T, T, s, 1,  c, ( "cm", fi[s] ) )
  return ( False, True, s, 0, c, ( "cm", "") )

def andmemo( m ):
  r = True
  for i in m:
    if not m[i]: r = False
  return r



outdata = ""

def output( s ):
  global outdata
  outdata = outdata + str(s)

def syntax_p( s, c):
  if been("syntax",s): return was( c, "syntax",s)
  else:
    mark("syntax",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      srules_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      end_p ( (ts+tl), tc)
 
    if ok:
      rv=syntax_s(a,andmemo(mem),s,ts+tl,tc,"syntax")
      return mark("syntax",s,rv)
    return mark("syntax",s,(F,T,s,0,c,("","")))

def srules_p( s, c):
  if been("srules",s): return was( c, "srules",s)
  else:
    mark("srules",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      srule_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      srules_p ( (ts+tl), tc)
 
    if ok:
      rv=srules_s(a,andmemo(mem),s,ts+tl,tc,"srules")
      return mark("srules",s,rv)
    return mark("srules",s,(F,T,s,0,c,("","")))

def srule_p( s, c):
  if been("srule",s): return was( c, "srule",s)
  else:
    mark("srule",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=blankline_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=base_p(s,c) 
    if not met:
      return mark("srule",s,(F,T,s,0,c,("","")))
    else:
      return mark("srule",s,(met,mem,s,tl,tc,ta)) 
def blankline_p( s, c):
  if been("blankline",s): return was( c, "blankline",s)
  else:
    mark("blankline",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=blankline_s(a,andmemo(mem),s,ts+tl,tc,"blankline")
      return mark("blankline",s,rv)
    return mark("blankline",s,(F,T,s,0,c,("","")))

def base_p( s, c):
  if been("base",s): return was( c, "base",s)
  else:
    mark("base",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      name_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      setup_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      body_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      recr_p ( (ts+tl), tc)
 
    if ok:
      rv=base_s(a,andmemo(mem),s,ts+tl,tc,"base")
      return mark("base",s,rv)
    return mark("base",s,(F,T,s,0,c,("","")))

def body_p( s, c):
  if been("body",s): return was( c, "body",s)
  else:
    mark("body",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=qlineset_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cline_p(s,c) 
    if not met:
      return mark("body",s,(F,T,s,0,c,("","")))
    else:
      return mark("body",s,(met,mem,s,tl,tc,ta)) 
def setup_p( s, c):
  if been("setup",s): return was( c, "setup",s)
  else:
    mark("setup",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm(':',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      setup_p ( (ts+tl), tc)
 
    if ok:
      rv=setup_s(a,andmemo(mem),s,ts+tl,tc,"setup")
      return mark("setup",s,rv)
    return mark("setup",s,(F,T,s,0,c,("","")))

def recr_p( s, c):
  if been("recr",s): return was( c, "recr",s)
  else:
    mark("recr",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('.',(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      name_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      rsetup_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      body_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      recr_p ( (ts+tl), tc)
 
    if ok:
      rv=recr_s(a,andmemo(mem),s,ts+tl,tc,"recr")
      return mark("recr",s,rv)
    return mark("recr",s,(F,T,s,0,c,("","")))

def rsetup_p( s, c):
  if been("rsetup",s): return was( c, "rsetup",s)
  else:
    mark("rsetup",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm(':',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      rcode_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      rsetup_p ( (ts+tl), tc)
 
    if ok:
      rv=rsetup_s(a,andmemo(mem),s,ts+tl,tc,"rsetup")
      return mark("rsetup",s,rv)
    return mark("rsetup",s,(F,T,s,0,c,("","")))

def rcode_p( s, c):
  if been("rcode",s): return was( c, "rcode",s)
  else:
    mark("rcode",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      ritm_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      rcode_p ( (ts+tl), tc)
 
    if ok:
      rv=rcode_s(a,andmemo(mem),s,ts+tl,tc,"rcode")
      return mark("rcode",s,rv)
    return mark("rcode",s,(F,T,s,0,c,("","")))

def ritm_p( s, c):
  if been("ritm",s): return was( c, "ritm",s)
  else:
    mark("ritm",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=string_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=rcr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=lwr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=dpathw_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=dhas_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=pnt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('>',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('<',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('{',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('}',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(':',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('%',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('(',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(',',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(')',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('_',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('[',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(']',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(';',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('+',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('-',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('*',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('/',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('=',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('!',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(' ',s,c) 
    if not met:
      return mark("ritm",s,(F,T,s,0,c,("","")))
    else:
      return mark("ritm",s,(met,mem,s,tl,tc,ta)) 
def cline_p( s, c):
  if been("cline",s): return was( c, "cline",s)
  else:
    mark("cline",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('^',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=cline_s(a,andmemo(mem),s,ts+tl,tc,"cline")
      return mark("cline",s,rv)
    return mark("cline",s,(F,T,s,0,c,("","")))

def qlineset_p( s, c):
  if been("qlineset",s): return was( c, "qlineset",s)
  else:
    mark("qlineset",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      qlines_p ( (ts+tl), tc)
 
    if ok:
      rv=qlineset_s(a,andmemo(mem),s,ts+tl,tc,"qlineset")
      return mark("qlineset",s,rv)
    return mark("qlineset",s,(F,T,s,0,c,("","")))

def qlines_p( s, c):
  if been("qlines",s): return was( c, "qlines",s)
  else:
    mark("qlines",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      qlsep_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      qline_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      qlines_p ( (ts+tl), tc)
 
    if ok:
      rv=qlines_s(a,andmemo(mem),s,ts+tl,tc,"qlines")
      return mark("qlines",s,rv)
    return mark("qlines",s,(F,T,s,0,c,("","")))

def qlsep_p( s, c):
  if been("qlsep",s): return was( c, "qlsep",s)
  else:
    mark("qlsep",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('|',(ts+tl), tc)
 
    if ok:
      rv=qlsep_s(a,andmemo(mem),s,ts+tl,tc,"qlsep")
      return mark("qlsep",s,rv)
    return mark("qlsep",s,(F,T,s,0,c,("","")))

def qline_p( s, c):
  if been("qline",s): return was( c, "qline",s)
  else:
    mark("qline",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      qchs_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=qline_s(a,andmemo(mem),s,ts+tl,tc,"qline")
      return mark("qline",s,rv)
    return mark("qline",s,(F,T,s,0,c,("","")))

def qchs_p( s, c):
  if been("qchs",s): return was( c, "qchs",s)
  else:
    mark("qchs",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      qch_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      qchs_p ( (ts+tl), tc)
 
    if ok:
      rv=qchs_s(a,andmemo(mem),s,ts+tl,tc,"qchs")
      return mark("qchs",s,rv)
    return mark("qchs",s,(F,T,s,0,c,("","")))

def qch_p( s, c):
  if been("qch",s): return was( c, "qch",s)
  else:
    mark("qch",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=aln_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=qq_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=qt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=qs_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=qsmb_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(' ',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=qcode_p(s,c) 
    if not met:
      return mark("qch",s,(F,T,s,0,c,("","")))
    else:
      return mark("qch",s,(met,mem,s,tl,tc,ta)) 
def qq_p( s, c):
  if been("qq",s): return was( c, "qq",s)
  else:
    mark("qq",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(34) ,(ts+tl), tc)
 
    if ok:
      rv=qq_s(a,andmemo(mem),s,ts+tl,tc,"qq")
      return mark("qq",s,rv)
    return mark("qq",s,(F,T,s,0,c,("","")))

def qt_p( s, c):
  if been("qt",s): return was( c, "qt",s)
  else:
    mark("qt",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(39) ,(ts+tl), tc)
 
    if ok:
      rv=qt_s(a,andmemo(mem),s,ts+tl,tc,"qt")
      return mark("qt",s,rv)
    return mark("qt",s,(F,T,s,0,c,("","")))

def qs_p( s, c):
  if been("qs",s): return was( c, "qs",s)
  else:
    mark("qs",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)
 
    if ok:
      rv=qs_s(a,andmemo(mem),s,ts+tl,tc,"qs")
      return mark("qs",s,rv)
    return mark("qs",s,(F,T,s,0,c,("","")))

def qcode_p( s, c):
  if been("qcode",s): return was( c, "qcode",s)
  else:
    mark("qcode",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('`',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('`',(ts+tl), tc)
 
    if ok:
      rv=qcode_s(a,andmemo(mem),s,ts+tl,tc,"qcode")
      return mark("qcode",s,rv)
    return mark("qcode",s,(F,T,s,0,c,("","")))

def name_p( s, c):
  if been("name",s): return was( c, "name",s)
  else:
    mark("name",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      lwr_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      name_p ( (ts+tl), tc)
 
    if ok:
      rv=name_s(a,andmemo(mem),s,ts+tl,tc,"name")
      return mark("name",s,rv)
    return mark("name",s,(F,T,s,0,c,("","")))
def name_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def qsmb_p( s, c):
  if been("qsmb",s): return was( c, "qsmb",s)
  else:
    mark("qsmb",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('-',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('_',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('+',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('=',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('~',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('!',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('@',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('#',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('$',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('%',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('^',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('&',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('!',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('|',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('/',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(':',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(';',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('*',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('(',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(')',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('[',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(']',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('{',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('}',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(',',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('.',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('<',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('>',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('?',s,c) 
    if not met:
      return mark("qsmb",s,(F,T,s,0,c,("","")))
    else:
      return mark("qsmb",s,(met,mem,s,tl,tc,ta)) 
def string_p( s, c):
  if been("string",s): return was( c, "string",s)
  else:
    mark("string",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(34) ,(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      strcs_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(34) ,(ts+tl), tc)
 
    if ok:
      rv=string_s(a,andmemo(mem),s,ts+tl,tc,"string")
      return mark("string",s,rv)
    return mark("string",s,(F,T,s,0,c,("","")))

def strcs_p( s, c):
  if been("strcs",s): return was( c, "strcs",s)
  else:
    mark("strcs",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      sch_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      strcs_p ( (ts+tl), tc)
 
    if ok:
      rv=strcs_s(a,andmemo(mem),s,ts+tl,tc,"strcs")
      return mark("strcs",s,rv)
    return mark("strcs",s,(F,T,s,0,c,("","")))

def code_p( s, c):
  if been("code",s): return was( c, "code",s)
  else:
    mark("code",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      citm_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)
 
    if ok:
      rv=code_s(a,andmemo(mem),s,ts+tl,tc,"code")
      return mark("code",s,rv)
    return mark("code",s,(F,T,s,0,c,("","")))

def citm_p( s, c):
  if been("citm",s): return was( c, "citm",s)
  else:
    mark("citm",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=string_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cnl_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=rcr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=lwr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=dpathw_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=dhas_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=pnt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('>',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('<',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('{',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('}',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(':',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('%',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('(',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(',',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(')',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('_',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('[',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(']',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(';',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('+',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('-',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('*',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('/',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('=',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('!',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(' ',s,c) 
    if not met:
      return mark("citm",s,(F,T,s,0,c,("","")))
    else:
      return mark("citm",s,(met,mem,s,tl,tc,ta)) 
def cnl_p( s, c):
  if been("cnl",s): return was( c, "cnl",s)
  else:
    mark("cnl",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('^',(ts+tl), tc)
 
    if ok:
      rv=cnl_s(a,andmemo(mem),s,ts+tl,tc,"cnl")
      return mark("cnl",s,rv)
    return mark("cnl",s,(F,T,s,0,c,("","")))

def dpathw_p( s, c):
  if been("dpathw",s): return was( c, "dpathw",s)
  else:
    mark("dpathw",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      dpath_p ( (ts+tl), tc)
 
    if ok:
      rv=dpathw_s(a,andmemo(mem),s,ts+tl,tc,"dpathw")
      return mark("dpathw",s,rv)
    return mark("dpathw",s,(F,T,s,0,c,("","")))

def dpath_p( s, c):
  if been("dpath",s): return was( c, "dpath",s)
  else:
    mark("dpath",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('.',(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      pnt_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      dpath_p ( (ts+tl), tc)
 
    if ok:
      rv=dpath_s(a,andmemo(mem),s,ts+tl,tc,"dpath")
      return mark("dpath",s,rv)
    return mark("dpath",s,(F,T,s,0,c,("","")))

def dhas_p( s, c):
  if been("dhas",s): return was( c, "dhas",s)
  else:
    mark("dhas",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('.',(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('.',(ts+tl), tc)
 
    if ok:
      rv=dhas_s(a,andmemo(mem),s,ts+tl,tc,"dhas")
      return mark("dhas",s,rv)
    return mark("dhas",s,(F,T,s,0,c,("","")))

def rcr_p( s, c):
  if been("rcr",s): return was( c, "rcr",s)
  else:
    mark("rcr",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=rca_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=rcb_p(s,c) 
    if not met:
      return mark("rcr",s,(F,T,s,0,c,("","")))
    else:
      return mark("rcr",s,(met,mem,s,tl,tc,ta)) 
def rca_p( s, c):
  if been("rca",s): return was( c, "rca",s)
  else:
    mark("rca",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('#',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      name_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm(':',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('#',(ts+tl), tc)
 
    if ok:
      rv=rca_s(a,andmemo(mem),s,ts+tl,tc,"rca")
      return mark("rca",s,rv)
    return mark("rca",s,(F,T,s,0,c,("","")))

def rcb_p( s, c):
  if been("rcb",s): return was( c, "rcb",s)
  else:
    mark("rcb",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('#',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      code_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('#',(ts+tl), tc)
 
    if ok:
      rv=rcb_s(a,andmemo(mem),s,ts+tl,tc,"rcb")
      return mark("rcb",s,rv)
    return mark("rcb",s,(F,T,s,0,c,("","")))

def end_p( s, c):
  if been("end",s): return was( c, "end",s)
  else:
    mark("end",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)
 
    if ok:
      rv=end_s(a,andmemo(mem),s,ts+tl,tc,"end")
      return mark("end",s,rv)
    return mark("end",s,(F,T,s,0,c,("","")))

def dgt_p( s, c):
  if been("dgt",s): return was( c, "dgt",s)
  else:
    mark("dgt",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('0',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('1',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('2',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('3',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('4',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('5',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('6',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('7',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('8',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('9',s,c) 
    if not met:
      return mark("dgt",s,(F,T,s,0,c,("","")))
    else:
      return mark("dgt",s,(met,mem,s,tl,tc,ta)) 
def upr_p( s, c):
  if been("upr",s): return was( c, "upr",s)
  else:
    mark("upr",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('A',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('B',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('C',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('D',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('E',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('F',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('G',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('H',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('I',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('J',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('K',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('L',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('M',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('N',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('O',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('P',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('Q',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('R',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('S',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('T',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('U',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('V',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('W',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('X',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('Y',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('Z',s,c) 
    if not met:
      return mark("upr",s,(F,T,s,0,c,("","")))
    else:
      return mark("upr",s,(met,mem,s,tl,tc,ta)) 
def lwr_p( s, c):
  if been("lwr",s): return was( c, "lwr",s)
  else:
    mark("lwr",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('a',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('b',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('c',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('d',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('e',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('f',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('g',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('h',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('i',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('j',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('k',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('l',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('m',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('n',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('o',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('p',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('q',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('r',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('s',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('t',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('u',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('v',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('w',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('x',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('y',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('z',s,c) 
    if not met:
      return mark("lwr",s,(F,T,s,0,c,("","")))
    else:
      return mark("lwr",s,(met,mem,s,tl,tc,ta)) 
def alp_p( s, c):
  if been("alp",s): return was( c, "alp",s)
  else:
    mark("alp",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=upr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=lwr_p(s,c) 
    if not met:
      return mark("alp",s,(F,T,s,0,c,("","")))
    else:
      return mark("alp",s,(met,mem,s,tl,tc,ta)) 
def aln_p( s, c):
  if been("aln",s): return was( c, "aln",s)
  else:
    mark("aln",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=upr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=lwr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=dgt_p(s,c) 
    if not met:
      return mark("aln",s,(F,T,s,0,c,("","")))
    else:
      return mark("aln",s,(met,mem,s,tl,tc,ta)) 
def hex_p( s, c):
  if been("hex",s): return was( c, "hex",s)
  else:
    mark("hex",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=dgt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('A',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('B',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('C',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('D',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('E',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('F',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('a',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('b',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('c',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('d',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('e',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('f',s,c) 
    if not met:
      return mark("hex",s,(F,T,s,0,c,("","")))
    else:
      return mark("hex",s,(met,mem,s,tl,tc,ta)) 
def smb_p( s, c):
  if been("smb",s): return was( c, "smb",s)
  else:
    mark("smb",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('-',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('_',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('+',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('=',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('`',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('~',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('!',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('@',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('#',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('$',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('%',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('^',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('&',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('|',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('/',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(':',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(';',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('*',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('(',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(')',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('[',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(']',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('{',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('}',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm(',',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('.',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('<',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('>',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('?',s,c) 
    if not met:
      return mark("smb",s,(F,T,s,0,c,("","")))
    else:
      return mark("smb",s,(met,mem,s,tl,tc,ta)) 
def sps_p( s, c):
  if been("sps",s): return was( c, "sps",s)
  else:
    mark("sps",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=bsl_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=btk_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=bqt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=bnl_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=btb_p(s,c) 
    if not met:
      return mark("sps",s,(F,T,s,0,c,("","")))
    else:
      return mark("sps",s,(met,mem,s,tl,tc,ta)) 
def bsl_p( s, c):
  if been("bsl",s): return was( c, "bsl",s)
  else:
    mark("bsl",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)
 
    if ok:
      rv=bsl_s(a,andmemo(mem),s,ts+tl,tc,"bsl")
      return mark("bsl",s,rv)
    return mark("bsl",s,(F,T,s,0,c,("","")))
def bsl_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def btk_p( s, c):
  if been("btk",s): return was( c, "btk",s)
  else:
    mark("btk",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(39) ,(ts+tl), tc)
 
    if ok:
      rv=btk_s(a,andmemo(mem),s,ts+tl,tc,"btk")
      return mark("btk",s,rv)
    return mark("btk",s,(F,T,s,0,c,("","")))
def btk_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def bqt_p( s, c):
  if been("bqt",s): return was( c, "bqt",s)
  else:
    mark("bqt",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(34) ,(ts+tl), tc)
 
    if ok:
      rv=bqt_s(a,andmemo(mem),s,ts+tl,tc,"bqt")
      return mark("bqt",s,rv)
    return mark("bqt",s,(F,T,s,0,c,("","")))
def bqt_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def bnl_p( s, c):
  if been("bnl",s): return was( c, "bnl",s)
  else:
    mark("bnl",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('n',(ts+tl), tc)
 
    if ok:
      rv=bnl_s(a,andmemo(mem),s,ts+tl,tc,"bnl")
      return mark("bnl",s,rv)
    return mark("bnl",s,(F,T,s,0,c,("","")))
def bnl_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def btb_p( s, c):
  if been("btb",s): return was( c, "btb",s)
  else:
    mark("btb",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(92) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('t',(ts+tl), tc)
 
    if ok:
      rv=btb_s(a,andmemo(mem),s,ts+tl,tc,"btb")
      return mark("btb",s,rv)
    return mark("btb",s,(F,T,s,0,c,("","")))
def btb_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def wsc_p( s, c):
  if been("wsc",s): return was( c, "wsc",s)
  else:
    mark("wsc",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm(' ',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('\t',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('\n',s,c) 
    if not met:
      return mark("wsc",s,(F,T,s,0,c,("","")))
    else:
      return mark("wsc",s,(met,mem,s,tl,tc,ta)) 
def s_p( s, c):
  if been("s",s): return was( c, "s",s)
  else:
    mark("s",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      sp_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)
 
    if ok:
      rv=s_s(a,andmemo(mem),s,ts+tl,tc,"s")
      return mark("s",s,rv)
    return mark("s",s,(F,T,s,0,c,("","")))
def s_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def sp_p( s, c):
  if been("sp",s): return was( c, "sp",s)
  else:
    mark("sp",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm(' ',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('\t',s,c) 
    if not met:
      return mark("sp",s,(F,T,s,0,c,("","")))
    else:
      return mark("sp",s,(met,mem,s,tl,tc,ta)) 
def sch_p( s, c):
  if been("sch",s): return was( c, "sch",s)
  else:
    mark("sch",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=dgt_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=upr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=lwr_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=smb_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=wsc_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=sps_p(s,c) 
    if not met:
      return mark("sch",s,(F,T,s,0,c,("","")))
    else:
      return mark("sch",s,(met,mem,s,tl,tc,ta)) 
def chs_p( s, c):
  if been("chs",s): return was( c, "chs",s)
  else:
    mark("chs",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      sch_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      chs_p ( (ts+tl), tc)
 
    if ok:
      rv=chs_s(a,andmemo(mem),s,ts+tl,tc,"chs")
      return mark("chs",s,rv)
    return mark("chs",s,(F,T,s,0,c,("","")))
def chs_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def pnt_p( s, c):
  if been("pnt",s): return was( c, "pnt",s)
  else:
    mark("pnt",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      dgt_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      pnt_p ( (ts+tl), tc)
 
    if ok:
      rv=pnt_s(a,andmemo(mem),s,ts+tl,tc,"pnt")
      return mark("pnt",s,rv)
    return mark("pnt",s,(F,T,s,0,c,("","")))
def pnt_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def als_p( s, c):
  if been("als",s): return was( c, "als",s)
  else:
    mark("als",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      aln_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      als_p ( (ts+tl), tc)
 
    if ok:
      rv=als_s(a,andmemo(mem),s,ts+tl,tc,"als")
      return mark("als",s,rv)
    return mark("als",s,(F,T,s,0,c,("","")))
def als_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def syntax_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "syntax", a[1][1] + a[2][1]  ))

def srules_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "srules", a[1][1] + a[2][1] ))

def blankline_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "blankline", "" ))

def base_s(a,m,s,e,c,n):

  rbody="  o = \"\"\n  rx="+a[2][1]+"_r\n  if a != \"\":\n"+a[5][1]+"  return (o)\n" 
  return (T,T,s,e-s,c,( "base", "\n" + \
"def " + a[2][1] + "_s(a,m,s,e,c,n):\n" + \
"" + ("  rx="+a[2][1]+"_r "  if a[5][1] != "" else "") + "\n" + \
"" + ("  "+a[3][1] if a[3][1] != "" else "") + "\n" + \
"  return (T,T,s,e-s,c,( \"" + a[2][1] + "\", " + a[4][1] + " ))\n" + \
"" + ("def "+a[2][1]+"_r(a,m,s,e,c,n):\n"+rbody if a[5][1] != "" else "") + "" ))

def setup_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "setup", ( ( a[4][1] + "\n  " + a[7][1]) if a[7][1] != "" else a[4][1] ) ))

def rsetup_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "rsetup", ( ( "      " + a[4][1] + "\n      " + a[7][1]+"\n") if a[7][1] != "" else "\n      "+a[4][1]+"\n" ) ))

def recr_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "recr", "    if a[0] ==\"" + a[3][1] + "\":\n" + a[4][1] + "      o=o+" + a[5][1] +"\n"+ a[6][1] ))

def cline_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "cline", a[4][1] ))

def qlineset_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qlineset", "\"" + a[1][1] + "\"" ))

def qlines_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qlines", a[2][1] + a[3][1] + a[4][1] ))

def qlsep_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qlsep", "\\n\" + \\\n\"" ))

def qline_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qline", a[1][1] ))

def qchs_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qchs", a[1][1] + a[2][1] ))

def qq_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qq", "\\\"" ))

def qt_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qt", "\\\'" ))

def qs_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qs", "\\\\" ))

def qcode_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "qcode", "\" + " + a[3][1] + " + \"" ))

def string_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "string", "\"" + a[2][1] + "\""   ))

def strcs_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "strcs", a[1][1] + a[2][1]    ))

def code_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "code", a[1][1]  + a[2][1]  ))

def rcode_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "rcode", a[1][1]  + a[2][1]  ))

def cnl_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "cnl", "\\\n" ))

def dpathw_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "dpathw", "a" + a[1][1] ))

def dpath_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "dpath", "[" + a[2][1] + "]" + a[3][1] ))

def dhas_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "dhas", "a"  ))

def rca_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "rca", a[3][1] +"_s(" + a[7][1] + ",m,s,e,c,n)[5][1]" ))

def rcb_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "rcb", "rx(" + a[3][1] + ",m,s,e,c,n)" ))


def end_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "end", "\n" + \

"prologue=\"\"\"import sys\n" + \
"from binascii import *\n" + \
"fi = file(sys.argv[1]).read()\n" + \
"semantics = file(sys.argv[2]).read()\n" + \
"fo = open(sys.argv[3], \"w+\")\n" + \
"\n" + \
"h={}; registers={}; context={}; mseq=0; dseq=1; T=True; F=False\n" + \
"\n" + \
"def n2z( a ):\n" + \
"  return ( \'0\' if a==\'\' else a )\n" + \
"\n" + \
"def be2le( a ):\n" + \
"  return a[6:8]+a[4:6]+a[2:4]+a[0:2]\n" + \
"\n" + \
"def mark( p, s, t ):\n" + \
"  ( v, m, ss, l, c, a ) = t\n" + \
"  if t[1]:  x = p +\"-\" + str(s);  h[x]=(v,m,l,a); return t\n" + \
"  else:\n" + \
"    if not t[0]:  x = p +\"-\" + str(s);  h[x]=(v,m,l,a); return t\n" + \
"  return t\n" + \
"\n" + \
"def been(p, s):\n" + \
" if h.has_key( p +\"-\" + str(s) ): return h[p +\"-\" + str(s)][1]\n" + \
" else:  return False\n" + \
"\n" + \
"def was(c,p,s): (v,m,l,a) = h[p+\"-\"+str(s)]; return (v,m,s,l,c,a) \n" + \
"\n" + \
"def cm( ch, s, c ):\n" + \
"  if s < len(fi):\n" + \
"    if fi[s] == ch:    return ( T, T, s, 1,  c, ( \"cm\", fi[s] ) )\n" + \
"  return ( False, True, s, 0, c, ( \"cm\", \"\") )\n" + \
"\n" + \
"def andmemo( m ):\n" + \
"  r = True\n" + \
"  for i in m:\n" + \
"    if not m[i]: r = False\n" + \
"  return r\n" + \
"\n" + \
"outdata = \"\"\n" + \
"\n" + \
"def output( s ):\n" + \
"  global outdata\n" + \
"  outdata = outdata + str(s)\n" + \
"\n" + \
"\"\"\"; epilogue=\"\"\"\n" + \
"\n" + \
"(v,m,s,l,c,a) = syntax_p( 0, ({},\'<1>\',\'<0>\') )\n" + \
"if v: \n" + \
"  print \"Parsed \"+a[0]+\" OK\"\n" + \
"else: print \"Failed to Parse\"\n" + \
"print >> fo, a[1] \n" + \
"fo.close()\n" + \
"\"\"\"" ))


def build (v,m,s,l,c,a): return 'success'

T=True; F=False

prologue = """import sys
from binascii import *

fi = file(sys.argv[1]).read()
semantics = file(sys.argv[2]).read()
fo = open(sys.argv[3], "w+")

h={}; registers={}; context={}; mseq=0; dseq=1; T=True; F=False

def n2z( a ):
  return ( '0' if a=='' else a )

def be2le( a ):
  return a[6:8]+a[4:6]+a[2:4]+a[0:2]

def mark( p, s, t ):
  ( v, m, ss, l, c, a ) = t
  if t[1]:  x = p +"-" + str(s);  h[x]=(v,m,l,a); return t
  else:
    if not t[0]:  x = p +"-" + str(s);  h[x]=(v,m,l,a); return t
  return t

def been(p, s):
 if h.has_key( p +"-" + str(s) ): return h[p +"-" + str(s)][1]
 else:  return False

def was(c,p,s): (v,m,l,a) = h[p+"-"+str(s)]; return (v,m,s,l,c,a) 

def cm( ch, s, c ):
  if s < len(fi):
    if fi[s] == ch:    return ( T, T, s, 1,  c, ( "cm", fi[s] ) )
  return ( False, True, s, 0, c, ( "cm", "") )

def andmemo( m ):
  r = True
  for i in m:
    if not m[i]: r = False
  return r

outdata = ""

def output( s ):
  global outdata
  outdata = outdata + str(s)

"""

epilogue = """

q3 = chr(34)+chr(34)+chr(34)
predefs = "prologue="+q3+prologue+q3+"; epilogue="+q3+epilogue+q3

(v,m,s,l,c,a) = syntax_p( 0, ({},'<1>','<0>') )
if v: 
  print "Parsed "+a[0]+" OK"
else: print "Failed to Parse"
print >> fo, a[1] 
fo.close()
"""

outdata = ""

def output( s ):
  global outdata
  outdata = outdata + str(s)

q3 = chr(34)+chr(34)+chr(34)
predefs = "prologue="+q3+prologue+q3+"; epilogue="+q3+epilogue+q3


(v,m,s,l,c,a) = syntax_p( 0, ({},'<1>','<0>') )
if v: 
  print "Parsed "+a[0]+" OK"
else: print "Failed to Parse"


print >> fo, a[1] 

fo.close()
