import sys
import os
import time
import random
import math

def gen_prime(p):
    if(p==2): return True
    if(not(p&1)): return False
    return pow(2,p-1,p)==1


def is_prime(x):
    if x >= 2:
        for y in range(2,int(round(math.sqrt(x)))):
            if not ( x % y ):
                return False
    else:
      return False
    return True


def primes(n):
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)
            n //= d
        d += 1
    if n > 1:
       primfac.append(n)
    return primfac


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m


#######################################



def chall_checkprime():
    p_np=random.randint(0,1)
    if p_np==0:
      primesize=15
      check_prime=0
      while check_prime == 0 :
        randomprime = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
        if gen_prime(randomprime):
          check_prime=1
          print "Is "+str(randomprime)+" prime (y/n)?"
          sys.stdout.flush()
          ans=raw_input("")
          if "y" in ans:
            print "Correct!"
          else:
            exit()


    else:
      primesize=15
      check_prime=0
      while check_prime == 0 :
        randomprime = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
        if not gen_prime(randomprime):
          check_prime=1
          print "Is "+str(randomprime)+" prime (y/n)?"
          sys.stdout.flush()
          ans=raw_input("")
          if "n" in ans:
            print "Correct!"
          else:
            exit() 


def chall_calculaten():
  p=0
  q=0
  check_prime=0
  primesize=15
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break
  print "p: "+str(p)
  print "q: "+str(q)
  print "Calculate N"
  sys.stdout.flush()
  ans_n=raw_input("")
  if int(ans_n) == (p*q):
    print "Correct!"
  else:
    exit()

def chall_factorn():
  p=0
  q=0
  check_prime=0
  primesize=7
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break

  print "N: "+str(p*q)
  print "Factorize N (Format: p,q)"
  sys.stdout.flush()
  ans_pq=raw_input("")
  p_ans=int(ans_pq.split(",")[0])
  q_ans=int(ans_pq.split(",")[1])
  if p_ans == p or p_ans == q:
    if q_ans == q or q_ans==p:
      print "Correct!"
    else:
      exit()
  else:
    exit()



######################################

def chall_computephi():
  p=0
  q=0
  check_prime=0
  primesize=15
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break
  print "p: "+str(p)
  print "q: "+str(q)
  print "Calculate the totient"
  sys.stdout.flush()
  ans_n=raw_input("")
  if int(ans_n) == ((p-1)*(q-1)):
    print "Correct!"
  else:
    exit()


def chall_computed():
  p=0
  q=0
  check_prime=0
  primesize=15
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break

  phi=(p-1)*(q-1)
  erange=[17, 257, 65537]
  re=random.randint(0,2)
  e=erange[re]
  cor_d=modinv(e,phi)
  if cor_d == -1:
    e=65537
    cor_d=modinv(e,phi)
    

  print "p: "+str(p)
  print "q: "+str(q)
  print "e: "+str(e)

  print "Calculate d"
  sys.stdout.flush()
  ans_d=raw_input("")
  
  if int(ans_d) == cor_d:
    print "Correct!"
  else:
    exit()


##################################################


def chall_encrypt():
  p=0
  q=0
  check_prime=0
  primesize=15
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break

  phi=(p-1)*(q-1)
  erange=[17, 257, 65537]
  re=random.randint(0,2)
  e=erange[re]
  phi=(p-1)*(q-1)
  d=modinv(e,phi)
  if d == -1:
    e=65537
    d=modinv(e,phi)
  
    

  print "p: "+str(p)
  print "q: "+str(q)
  print "e: "+str(e)

  
  
  wordlist=['began','idea','fish','mountain','stop','once','base','hear','horse','cut','sure','watch','color','face','wood','main','enough','plain','girl','usual','young','ready','above','ever','red','list','though','feel','talk','bird','soon','body','dog','family','direct','pose','leave','song','measure','door','product','black','short','numeral','class','wind','question','happen','complete','ship','area','half','rock','order','fire','south','problem','piece','told','knew','pass','since','top','whole','king','space','heard','best','hour','better','true','during','hundred','five','remember','step','early','hold','west','ground','interest','reach','fast','verb','sing','listen','six','table','travel','less','morning','ten','simple','several','vowel','toward','war','lay','against','pattern','slow','center','love','person','money','serve','appear','road','map','rain','rule','govern','pull','cold','notice','voice','unit','power','town','fine','certain','fly','fall','lead','cry','dark','machine','note','wait','plan','figure','star','box','noun','field','rest','correct','able','pound','done','beauty','drive','stood','contain','front','teach','week','final','gave','green','oh','quick','develop','ocean','warm','free','minute','strong','special','mind','behind','clear','tail','produce','fact','street','inch','multiply','nothing','course','stay','wheel','full','force','blue','object','decide','surface','deep','moon','island','foot','system','busy','test','record','boat','common','gold','possible','plane','stead','dry','wonder','laugh','thousand','ago','ran','check','game','shape','equate','hot','miss','brought','heat','snow','tire','bring','yes','distant','fill','east','paint','language','among','grand','ball','yet','wave','drop','heart','am','present','heavy','dance','engine','position','arm','wide','sail','material','size','vary','settle','speak','weight','general','ice','matter','circle','pair','include','divide','syllable','felt','perhaps','pick','sudden','count','square','reason']
  rword=wordlist[random.randint(0,251)]

  print "Encrypt '"+rword+"' without the quotes"
  sys.stdout.flush()
  ans_c=raw_input("")
  
  N=p*q
  phi=(p-1)*(q-1)
  m=int(rword.encode('hex'),16)
  cor_c=pow(m,e,N)

  
  if int(ans_c) == cor_c:
    print "Correct!"
  else:
    exit()





def chall_decrypt():
  p=0
  q=0
  check_prime=0
  primesize=15
  while check_prime == 0 :
    randomnumber = random.randrange(math.pow(10,primesize-1),math.pow(10,primesize)-1)
    if gen_prime(randomnumber):
        if p == 0:
          p=randomnumber
        elif not p == 0 and q == 0:
          q=randomnumber
        elif not p == 0 and not q == 0:
          check_prime=1
          break

  phi=(p-1)*(q-1)
  erange=[17, 257, 65537]
  re=random.randint(0,2)
  e=erange[re]

  
  
  wordlist=['began','idea','fish','mountain','stop','once','base','hear','horse','cut','sure','watch','color','face','wood','main','enough','plain','girl','usual','young','ready','above','ever','red','list','though','feel','talk','bird','soon','body','dog','family','direct','pose','leave','song','measure','door','product','black','short','numeral','class','wind','question','happen','complete','ship','area','half','rock','order','fire','south','problem','piece','told','knew','pass','since','top','whole','king','space','heard','best','hour','better','true','during','hundred','five','remember','step','early','hold','west','ground','interest','reach','fast','verb','sing','listen','six','table','travel','less','morning','ten','simple','several','vowel','toward','war','lay','against','pattern','slow','center','love','person','money','serve','appear','road','map','rain','rule','govern','pull','cold','notice','voice','unit','power','town','fine','certain','fly','fall','lead','cry','dark','machine','note','wait','plan','figure','star','box','noun','field','rest','correct','able','pound','done','beauty','drive','stood','contain','front','teach','week','final','gave','green','oh','quick','develop','ocean','warm','free','minute','strong','special','mind','behind','clear','tail','produce','fact','street','inch','multiply','nothing','course','stay','wheel','full','force','blue','object','decide','surface','deep','moon','island','foot','system','busy','test','record','boat','common','gold','possible','plane','stead','dry','wonder','laugh','thousand','ago','ran','check','game','shape','equate','hot','miss','brought','heat','snow','tire','bring','yes','distant','fill','east','paint','language','among','grand','ball','yet','wave','drop','heart','am','present','heavy','dance','engine','position','arm','wide','sail','material','size','vary','settle','speak','weight','general','ice','matter','circle','pair','include','divide','syllable','felt','perhaps','pick','sudden','count','square','reason']
  rword=wordlist[random.randint(0,251)]

  ###
  N=p*q
  #phi=(p-1)*(q-1)
  #d=modinv(e,phi)
  m=int(rword.encode('hex'),16)
  c=pow(m,e,N)
  ###

  print "N: "+str(N)
  print "e: "+str(e)
  print "c: "+str(c)

  print "Decrypt the word"
  
  sys.stdout.flush()
  ans_m=raw_input("")
  
  if ans_m == str(rword):
    print "Correct!"
  else:
    exit()





def main():
  print "You think you understand RSA!"
  print "Prove it! You have to solve 20 tasks in 3 different stages. Do it by hand or automate it. Good luck!"
  print ""
  print "------Stage 1------"
  count1=0
  stage1t=9 #9
  
  while count1 <=stage1t:
    r=random.randint(0,2)  
    if r == 0:
      chall_checkprime()
    elif r == 1:
      chall_calculaten()
    elif r == 2:
      chall_factorn()

    count1+=1
  print ""

  print "------Stage 2------"
  count2=0
  stage2t=5 #5
  while count2 <=stage2t:
    r=random.randint(0,1)  
    if r == 0:
      chall_computephi()
    elif r == 1:
      chall_computed()
    

    count2+=1
  print ""

  print "------Stage 3------"
  count3=0
  stage3t=3 #3
  while count3 <=stage3t:
    r=random.randint(0,1)  
    if r == 0:
      chall_encrypt()
    elif r == 1:
      chall_decrypt()
    

    count3+=1
  print ""

  print "------Stage 4------"
  pubkey="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d4949427744414e42676b71686b6947397730424151454641414f43416130414d49494271414b423051635a694673623759317132766656346e7961526e41640a5836356234516563446c4d2f6a6e3259566279686243482f5a663069716c526f7375644a396c36624c44747074417063647758433143584f6252496841614e700a70426f6671527433494e63387a2b48314974373331355268356e676b36515249725938765a796a54397572496a7157375938703841724f7a327353542f75532f0a4871714263626d5950762f4f70436156637759355536617974774f4b335a72617a4c6e502f6b496e6f35354b613834676172524c517834303832365052734d580a4c6943574166437131436d5341564c306d6f4d6f4e664653597179576838745968577875644437736256566d4b3169615a4e4c37575232704c64425a3550564a0a416f4852426535374e646d4c7071547361763063362f686964684b797556322f534c413042375230567634587a34316b5636524a676a46454134504d49676d740a4b2b686a474c49786e314a677a7a77354c356255304a6638644838594d314451763438784274476b49355543674b68386c6c506c666f733241346278374b41430a58743862777a7257792f4d5750464d43654936753835646f73542f4376554b637573634e626b3541497557325744394d38677268436754694f7a4e734f7241680a656a506139363932395545597564725077646e525436514c7875556845745a305662736d4176556a4a4e5546414e5a5979775376457654512b7079556c6178760a4953782f6a6743784138494e6b54634c534a4d4435396c724a49553d0a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
  print "I came across this encrypted message. See if you can decrypt it for me."
  print ""
  print pubkey.decode('hex')
  print "Message: (hex)"
  c=2721702567693195824155631413288135657660627479214148614554599244990778156020719699327930449877732884715856137641573576870481972782415652111324694656745696090015573698515448525575077918159061834625574626487010186438603208505597632913908295084322053444909137093037793792365665256069416257343792027073604973628078509075503997356820762367862749779031901268976433560661391136143606203928292959587330613478296541353140157170276345846281307157460267945548698454232613066491977938211299370738657124942385141694
  print hex(c)[2:-1]


if __name__ == "__main__":
  try:
    main()
  except:
    pass
