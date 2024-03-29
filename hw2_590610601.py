cipher=[0b111111,0b10010000,0b111,0b11101,0b1111110,0b111,0b11101,0b111,0b1111110,0b1111110,0b10010000,0b10101001,0b111,0b11111110,0b111,0b10010000,0b1011000,0b10101001,0b10010000,0b10111111,0b10111111,0b1100010,0b10010000,0b111,0b1111110,0b10010000,0b1011000,0b10101001,0b111111,0b10111111,0b1100010,0b11111110,0b111111,0b111,0b10111111,0b11101,0b10010000,0b1011000,0b111111,0b1011000,0b111,0b11111110,0b10010000,0b11111110,0b11101,0b1011000,0b11111110,0b10101001,0b10010000,0b10010000,0b111,0b11101,0b10101001,0b111111,0b10101001,0b1011000,0b11101,0b10101001,0b111,0b111,0b11101,0b1111110,0b10010000,0b11101,0b10111111,0b111,0b11111110,0b111,0b111111,0b111111,0b111,0b1011000,0b11111110,0b111111,0b11101,0b1111110,0b1011000 ]
plain_stdID="590610601"
plain_stdID=plain_stdID.encode('utf-8')

cipher_block_size=8
key_block_size=10
subkeys_block_size=8

# ------------------------------------------    
def extendTo8Bits(m,nbit=8):
  b_str=str(bin(m)) #bin(m)
  b_str=b_str[2:len(b_str)]  # to get rid of 0b.....
  temp_0=""
  for i in range(nbit-len(b_str)):
    temp_0+="0"
  b_str=temp_0+b_str  
  return b_str
# ------------------------------------------ 
def swapBit(m,seq):
  x=""
  for i in seq:
    x+=m[i-1]
  return x  
# ------------------------------------------ 
def IP(ci):
  b_str=extendTo8Bits(ci)
  sequence=[2,6,3,1,4,8,5,7]
  return swapBit(b_str,sequence)
# ------------------------------------------ 
def EP(m):
  sequence=[4,1,2,3,2,3,4,1]
  return swapBit(m,sequence)
# ------------------------------------------ 
def XOR8bit(m,key):
  x=""
  key=extendTo8Bits(key)
  for i in range(len(key)):
    x+=str( int(m[i])^int(key[i]) )
  return x
# ------------------------------------------ 
def XOR4bit(m1,m2):
  x=""
  for i in range(len(m1)):
    x+=str( int(m1[i])^int(m2[i]) )
  return x
# ------------------------------------------ 
def SBox(m):
  s0=[["01","00","11","10"],["11","10","01","00"],["00","10","01","11"],["11","01","11","10"]]
  s1=[["00","01","10","11"],["10","00","01","11"],["11","00","01","00"],["10","01","00","11"]]
  L4bit=m[0:4]
  R4bit=m[4:8]
  row=int(L4bit[0]+L4bit[3],base=2)
  col=int(L4bit[1]+L4bit[2],base=2)
  r_s0=s0[row][col]
  row=int(R4bit[0]+R4bit[3],base=2)
  col=int(R4bit[1]+R4bit[2],base=2)
  r_s1=s1[row][col]
  return r_s0+r_s1
# ------------------------------------------ 
def P4(m):
  sequence=[2,4,3,1]
  return swapBit(m,sequence)
# ------------------------------------------
def IPinv(m):
  sequence=[4,1,3,5,7,2,8,6]
  return swapBit(m,sequence)
# ------------------------------------------ 
def SDESDecrypt(m,sk1,sk2):
  r1 = IP(m)  #IP return string / m is int base10
  r2 = EP(r1[4:8])
  r3 = XOR8bit(r2,sk2)   # return string
  r4 = SBox(r3)
  r5 = P4(r4)
  r6 = XOR4bit(r1[0:4],r5)
  r7 = r6 + r1[4:8]
  r8 = r7[4:8] + r7[0:4]
  r9 = EP(r8[4:8])
  r10= XOR8bit(r9,sk1)
  r11= SBox(r10)
  r12= P4(r11)
  r13= XOR4bit(r12,r8[0:4])
  r14= r13 + r8[4:8]
  return IPinv(r14)
def SDESEncrypt(m,sk1,sk2):
  r1 = IP(m)  #IP return string
  r2 = EP(r1[4:8])
  r3 = XOR8bit(r2,sk1)   # return string
  r4 = SBox(r3)
  r5 = P4(r4)
  r6 = XOR4bit(r1[0:4],r5)
  r7 = r6 + r1[4:8]
  r8 = r7[4:8] + r7[0:4]
  r9 = EP(r8[4:8])
  r10= XOR8bit(r9,sk2)
  r11= SBox(r10)
  r12= P4(r11)
  r13= XOR4bit(r12,r8[0:4])
  r14= r13 + r8[4:8]
  return IPinv(r14)
# ------------------------------------------  
def guessSubKeys(ci,txt):
  subkeys=[None for i in range(2)]
  subkey1=-1
  subkey2=-1
  
  for j in range(256): 
    subkey1=j
    for k in range(256):
      subkey2=k
      miss=0
      for ii in range(len(ci)):
        test_subkey=SDESDecrypt(ci[ii],subkey1,subkey2)
        
        if int(test_subkey,base=2) != int(txt[ii]):
          break
        if ii==len(ci)-1 :
          subkeys[0]=subkey1
          subkeys[1]=subkey2
          return subkeys
          
  print("No key found.")
  return None
# ------------------------------------------ 
def P10(k):
  sequence=[3,5,2,7,4,10,1,9,8,6]
  return swapBit(k,sequence)
def P8(k):
  sequence=[6,3,7,4,8,5,10,9]
  return swapBit(k,sequence)
def rotateShift(k,nbit):
  if nbit==1:
    sequence=[1,2,3,4,0]
  if nbit==3:
    sequence=[3,4,0,1,2]
  return swapBit(k,sequence)
def getKey(sk1,sk2):
  for i in range(1024): # key has 10 bits
    key=extendTo8Bits(i,10)   #output string 10 bits
    r1 = P10(key)
    r2 = str(rotateShift(r1[0:5],1)) + str(rotateShift(r1[5:10],1))
    k1 = P8(r2)
    r2 = str(rotateShift(r1[0:5],3)) + str(rotateShift(r1[5:10],3))
    k2 = P8(r2)
    if int(k1,base=2)==sk1 and int(k2,base=2)==sk2 or int(k1,base=2)==sk2 and int(k2,base=2)==sk1:
      return key    
################ MAIN ####################
# 1-guest the key
#   from clue : first 9 block of cipher is my student ID
sub_keys = [None for i in range(2)]
sub_keys = guessSubKeys(cipher[0:9],plain_stdID)

key = getKey(sub_keys[0],sub_keys[1])
print("Key : "+str(key))
print("Subkey[1] : "+str(sub_keys[0])+" , Subkey[2]: "+str(sub_keys[1]))
# decrypt all 
ans=[]
for i in range(len(cipher)):
  temp=int(SDESDecrypt(cipher[i],sub_keys[0],sub_keys[1]),base=2)
  ans.append(chr(temp))
print(ans)
##########################################
