#!/usr/bin/env python3
from pathlib import Path
import hashlib, struct, sys

EXPECTED_SHA1 = "c0ff3999e1093e1af59ef3eea3f1bfd7c1f18a65"
RESERVED = [0x6A,0x73,0x74,0x75,0x76,0x77,0x7C,0x7D,0x7E]

def gb_global_checksum(buf):
    return (sum(buf[0:0x14E]) + sum(buf[0x150:])) & 0xFFFF

def main(srcname, outname):
    src=Path(srcname); out=Path(outname)
    b=bytearray(src.read_bytes())
    if hashlib.sha1(b).hexdigest()!=EXPECTED_SHA1:
        raise SystemExit("Refusing to patch: source SHA-1 does not match Korean Gold reference ROM")
    for bank in RESERVED:
        if any(b[bank*0x4000:(bank+1)*0x4000]):
            raise SystemExit(f"Refusing to patch: reserved bank {bank:02X} is not empty")
    base=0x6A*0x4000
    h=bytearray(0x100)
    h[:8]=b"GOLD1025"
    struct.pack_into('<HHH',h,8,1,1025,251)
    h[0x0E:0x12]=bytes([0xFC,0xFD,32,0x07])
    h[0x12:0x26]=bytes.fromhex(EXPECTED_SHA1)
    struct.pack_into('<I',h,0x28,0x51BDF)
    struct.pack_into('<HHHH',h,0x2C,29,30,252,774)
    descs=[
      (b'BST1',0x73,0x01,0x4000,512*32),(b'BST2',0x74,0x01,0x4000,262*32),
      (b'NAME',0x75,0x06,0x4000,0x4000),(b'EVOL',0x76,0x06,0x4000,0x4000),
      (b'LEVL',0x77,0x06,0x4000,0x4000),(b'DEX1',0x7C,0x06,0x4000,0x4000),
      (b'DEX2',0x7D,0x06,0x4000,0x4000),(b'GFXI',0x7E,0x06,0x4000,0x4000)]
    h[0x34]=len(descs); p=0x40
    for tag,bank,flags,addr,cap in descs:
      h[p:p+4]=tag; h[p+4]=bank; h[p+5]=flags
      struct.pack_into('<HI',h,p+6,addr,cap); p+=12
    b[base:base+0x100]=h
    index=b''.join(struct.pack('<HH',n,n-252) for n in range(252,1026))
    b[base+0x100:base+0x100+len(index)]=index
    b[0x14E:0x150]=b'\0\0'
    chk=gb_global_checksum(b)
    b[0x14E:0x150]=chk.to_bytes(2,'big')
    out.write_bytes(b)
    print('output',out)
    print('sha1',hashlib.sha1(b).hexdigest())
    print('global_checksum',f'{chk:04x}')

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit(f"usage: {sys.argv[0]} SOURCE.gbc OUTPUT.gbc")
    main(sys.argv[1],sys.argv[2])
