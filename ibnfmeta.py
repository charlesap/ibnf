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
      rules_p ( (ts+tl), tc)
 
    if ok:
      rv=syntax_s(a,andmemo(mem),s,ts+tl,tc,"syntax")
      return mark("syntax",s,rv)
    return mark("syntax",s,(F,T,s,0,c,("","")))

def rules_p( s, c):
  if been("rules",s): return was( c, "rules",s)
  else:
    mark("rules",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      rule_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      rules_p ( (ts+tl), tc)
 
    if ok:
      rv=rules_s(a,andmemo(mem),s,ts+tl,tc,"rules")
      return mark("rules",s,rv)
    return mark("rules",s,(F,T,s,0,c,("","")))

def rule_p( s, c):
  if been("rule",s): return was( c, "rule",s)
  else:
    mark("rule",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=incorp_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=altern_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=blankline_p(s,c) 
    if not met:
      return mark("rule",s,(F,T,s,0,c,("","")))
    else:
      return mark("rule",s,(met,mem,s,tl,tc,ta)) 
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

def altern_p( s, c):
  if been("altern",s): return was( c, "altern",s)
  else:
    mark("altern",s,(F,T,s,0,c,("",""))) 
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
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('?',(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      albody_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm(';',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=altern_s(a,andmemo(mem),s,ts+tl,tc,"altern")
      return mark("altern",s,rv)
    return mark("altern",s,(F,T,s,0,c,("","")))

def incorp_p( s, c):
  if been("incorp",s): return was( c, "incorp",s)
  else:
    mark("incorp",s,(F,T,s,0,c,("",""))) 
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
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      iflag_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      inbody_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm(';',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=incorp_s(a,andmemo(mem),s,ts+tl,tc,"incorp")
      return mark("incorp",s,rv)
    return mark("incorp",s,(F,T,s,0,c,("","")))

def iflag_p( s, c):
  if been("iflag",s): return was( c, "iflag",s)
  else:
    mark("iflag",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=cm('/',s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cm('=',s,c) 
    if not met:
      return mark("iflag",s,(F,T,s,0,c,("","")))
    else:
      return mark("iflag",s,(met,mem,s,tl,tc,ta)) 
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
def albody_p( s, c):
  if been("albody",s): return was( c, "albody",s)
  else:
    mark("albody",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      nit_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      almore_p ( (ts+tl), tc)
 
    if ok:
      rv=albody_s(a,andmemo(mem),s,ts+tl,tc,"albody")
      return mark("albody",s,rv)
    return mark("albody",s,(F,T,s,0,c,("","")))

def almore_p( s, c):
  if been("almore",s): return was( c, "almore",s)
  else:
    mark("almore",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('|',(ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      alnewline_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      albody_p ( (ts+tl), tc)
 
    if ok:
      rv=almore_s(a,andmemo(mem),s,ts+tl,tc,"almore")
      return mark("almore",s,rv)
    return mark("almore",s,(F,T,s,0,c,("","")))

def alnewline_p( s, c):
  if been("alnewline",s): return was( c, "alnewline",s)
  else:
    mark("alnewline",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(10) ,(ts+tl), tc)
 
    if ok:
      rv=alnewline_s(a,andmemo(mem),s,ts+tl,tc,"alnewline")
      return mark("alnewline",s,rv)
    return mark("alnewline",s,(F,T,s,0,c,("","")))
def alnewline_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))
def inbody_p( s, c):
  if been("inbody",s): return was( c, "inbody",s)
  else:
    mark("inbody",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      s_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      onit_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( nok,mem[n],ts,tl,tc,a[n])=\
      inbody_p ( (ts+tl), tc)
 
    if ok:
      rv=inbody_s(a,andmemo(mem),s,ts+tl,tc,"inbody")
      return mark("inbody",s,rv)
    return mark("inbody",s,(F,T,s,0,c,("","")))

def onit_p( s, c):
  if been("onit",s): return was( c, "onit",s)
  else:
    mark("onit",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=pnit_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=nit_p(s,c) 
    if not met:
      return mark("onit",s,(F,T,s,0,c,("","")))
    else:
      return mark("onit",s,(met,mem,s,tl,tc,ta)) 
def pnit_p( s, c):
  if been("pnit",s): return was( c, "pnit",s)
  else:
    mark("pnit",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      cm('.',(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      nit_p ( (ts+tl), tc)
 
    if ok:
      rv=pnit_s(a,andmemo(mem),s,ts+tl,tc,"pnit")
      return mark("pnit",s,rv)
    return mark("pnit",s,(F,T,s,0,c,("","")))

def nit_p( s, c):
  if been("nit",s): return was( c, "nit",s)
  else:
    mark("nit",s,(F,T,s,0,c,("","")));met = F 

    if not met: (met,mem,ts,tl,tc,ta)=name_p(s,c)
    if not met: (met,mem,ts,tl,tc,ta)=cmatch_p(s,c) 
    if not met:
      return mark("nit",s,(F,T,s,0,c,("","")))
    else:
      return mark("nit",s,(met,mem,s,tl,tc,ta)) 
def cmatch_p( s, c):
  if been("cmatch",s): return was( c, "cmatch",s)
  else:
    mark("cmatch",s,(F,T,s,0,c,("",""))) 
    ok=True; ts=s; tl=0; a={0: ("","")}
    mem={0:True}; tc=c; n=0

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(39) ,(ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
      sch_p ( (ts+tl), tc)

    if ok:
      n=n+1; ( ok,mem[n],ts,tl,tc,a[n])=\
       cm(chr(39) ,(ts+tl), tc)
 
    if ok:
      rv=cmatch_s(a,andmemo(mem),s,ts+tl,tc,"cmatch")
      return mark("cmatch",s,rv)
    return mark("cmatch",s,(F,T,s,0,c,("","")))

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
  return (T,T,s,e-s,c,( "syntax", prologue + a[1][1] + semantics + epilogue  ))

def rules_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "rules", a[1][1] + a[2][1]  ))

def blankline_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "blankline", ""  ))



def altern_s(a,m,s,e,c,n):

  rx=altern_r ;  return (T,T,s,e-s,c,( "altern", "\n" + \
"def " + a[2][1] + "_p( s, c):\n" + \
"  if been(\"" + a[2][1] + "\",s): return was( c, \"" + a[2][1] + "\",s)\n" + \
"  else:\n" + \
"    mark(\"" + a[2][1] + "\",s,(F,T,s,0,c,(\"\",\"\")));met = F \n" + \
"" + rx(a[5],m,s,e,c,n) + " \n" + \
"    if not met:\n" + \
"      return mark(\"" + a[2][1] + "\",s,(F,T,s,0,c,(\"\",\"\")))\n" + \
"    else:\n" + \
"      return mark(\"" + a[2][1] + "\",s,(met,mem,s,tl,tc,ta)) " ))
def altern_r(a,m,s,e,c,n):
  o = ""
  rx=altern_r
  if a != "":
    if a[0] =="albody":
      o=o+rx(a[1][2],m,s,e,c,n)  + rx(a[1][3][1],m,s,e,c,n)
    if a[0] =="cmatch":
      o=o+rx(a[1],m,s,e,c,n)
    if a[0] =="cm":
      o=o+"\n" + \
"    if not met: (met,mem,ts,tl,tc,ta)=cm(\'" + a[1] + "\',s,c)"
    if a[0] =="btb":
      o=o+"\n" + \
"    if not met: (met,mem,ts,tl,tc,ta)=cm(\'" + a[1] + "\',s,c)"
    if a[0] =="bnl":
      o=o+"\n" + \
"    if not met: (met,mem,ts,tl,tc,ta)=cm(\'" + a[1] + "\',s,c)"
    if a[0] =="name":
      o=o+"\n" + \
"    if not met: (met,mem,ts,tl,tc,ta)=" + a[1] + "_p(s,c)"
  return (o)


def incorp_s(a,m,s,e,c,n):
  smfnc="_s(a,m,s,e,c,n): return(T,T,s,e-s,c,(n,fi[s:e]))"
  rx=incorp_r ;  return (T,T,s,e-s,c,( "incorp", "\n" + \
"def " + a[2][1] + "_p( s, c):\n" + \
"  if been(\"" + a[2][1] + "\",s): return was( c, \"" + a[2][1] + "\",s)\n" + \
"  else:\n" + \
"    mark(\"" + a[2][1] + "\",s,(F,T,s,0,c,(\"\",\"\"))) \n" + \
"    ok=True; ts=s; tl=0; a={0: (\"\",\"\")}\n" + \
"    mem={0:True}; tc=c; n=0\n" + \
"" + rx(a[5],m,s,e,c,n) + " \n" + \
"    if ok:\n" + \
"      rv=" + a[2][1] + "_s(a,andmemo(mem),s,ts+tl,tc,\"" + a[2][1] + "\")\n" + \
"      return mark(\"" + a[2][1] + "\",s,rv)\n" + \
"    return mark(\"" + a[2][1] + "\",s,(F,T,s,0,c,(\"\",\"\")))\n" + \
"" + ("def "+a[2][1]+smfnc if a[4][1] == "/" else "") + "" ))
def incorp_r(a,m,s,e,c,n):
  o = ""
  rx=incorp_r
  if a != "":
    if a[0] =="inbody":
      o=o+"\n" + \
"    if ok:\n" + \
"      n=n+1; ( " + (  "n" if a[1][2][0] == "pnit" else "" ) + "ok,mem[n],ts,tl,tc,a[n])=\\\n" + \
"      " + rx(a[1][2][1] if a[1][2][0]=="pnit" else a[1][2],m,s,e,c,n) + "\n" + \
"" + rx(a[1][3],m,s,e,c,n) + ""
    if a[0] =="pnit":
      o=o+"n"
    if a[0] =="cmatch":
      o=o+rx(a[1],m,s,e,c,n) 
    if a[0] =="name":
      o=o+a[1] +"_p ( (ts+tl), tc)"
    if a[0] =="cm":
      o=o+"cm(\'" + a[1] + "\',(ts+tl), tc)"
    if a[0] =="bsl":
      o=o+" cm(chr(92) ,(ts+tl), tc)"
    if a[0] =="btk":
      o=o+" cm(chr(39) ,(ts+tl), tc)"
    if a[0] =="bqt":
      o=o+" cm(chr(34) ,(ts+tl), tc)"
    if a[0] =="bnl":
      o=o+" cm(chr(10) ,(ts+tl), tc)"
  return (o)


def almore_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "almore", a[4] ))

def albody_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "albody", a ))

def inbody_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "inbody", a  ))

def pnit_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "pnit", a[2]  ))

def cmatch_s(a,m,s,e,c,n):
  return (T,T,s,e-s,c,( "cmatch", a[2]  ))


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
(v,m,s,l,c,a) = syntax_p( 0, ({},'<1>','<0>') )
if v: 
  print "Parsed "+a[0]+" OK"
else: print "Failed to Parse"


print >> fo, a[1] 

fo.close()"""

outdata = ""

def output( s ):
  global outdata
  outdata = outdata + str(s)




(v,m,s,l,c,a) = syntax_p( 0, ({},'<1>','<0>') )
if v: 
  print "Parsed "+a[0]+" OK"
else: print "Failed to Parse"
print >> fo, a[1] 
fo.close()
