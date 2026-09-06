#!/usr/bin/env python3
"""Recover Korean Silver ROM bank $57 / Map Scripts 22.

Provenance:
  Pocket Monsters Eun (Korea).gbc
  SHA-1 cb22d7e03a74dc3a563fde6be8626626b2b392e7

Verification before generation:
  134/134 TX text command streams re-encoded byte-identically (8,813 bytes).
  16 raw menu strings re-encoded byte-identically (235 bytes).
"""
from pathlib import Path
import base64, json, re, sys, zlib

DATA = r"""c-p;P|4$o9mj73p{B$c#ZYN*wv^re|2$1ZCgah`Xl}3tspb1vM&9zOk>}n(f9mc`V#0)l=#AeLK#1J_*2293m%#E~v%H417^8aw}RaLjUtE!E&C*5q6fV<sQ_3C~3yw7{p`{zrRu`n0A^qW6ln%5U%zaBB?rj4j&PLC|j|Dzt8#|sZ<Bk`!QG+@k_mN9AkF@EVcm%fh2;Ro&OOO9Q>Otv$9Utjt<`gMFR5;gF{m3pg|(41P<*(+$R<_BjZ)5mXF&@CNrd4B*OYVB85(%f|3SG9I7-#RI2WH(86w@A(w9+-Dt*&0a|$nHivS9eb8PAb_tOS8MC%qX49hs<S-Y}@4cgVy>vLAI;pO`6z+;K-!VyiAH48a$Ac>~^ly`fC#&b}KkwC4<9kWLn21XFcn@tZ6WZz-aD3wH!>{NgX(;G9PH#j2d4@FMZ)kZerG4oSTlu2aE}G!muLdVoVexd0m4)|DAXTe*&{*A89aYlH2JM#B3*>Y8~dOxj(@?%B|C?AZxO^?4)5k-hV<NAD75hU3gNfS#>H&CQ|<-#FhNPTpTs@Xhc#2vXk)5&mDIsaasP9uc!@MbNG_~6POIY!CPHlh*%%a>haqqOzEK>jf)dv5Ai?URlE-wl55`5K*dO9S#v&Qsj99VkX#-F6I27dDQANs*GMICEBKtB8YGuQ;e*VagEO+7#6Mg0-~)Cuno~-)el9ydR@q~MN>r@3jzG668Tbh<ic1}v)0Yfu+?X;VPmO8#EfO8jryoo5|Ch0Q{eKu5|5wn}e;~!guei~H`8gjGZMzoKo8W|;{U)sN4WZf-BJ1#x6%PY}!cVR>7n;tYAe2-C^}UjSO;{&IkZ&#xJ_HOhAe&ab?v(aPF|V~6HIgjhon*72kz^hp49^eT?zs~D23aq+vrT8SfNsM%J8+6kQn8tp2DdSv(Qp%vSE++3+pSOe5E=Bx<CZ=pX&N{?^7_!JHbL%Md%NuH9kIXRu`n!(0kk9_fWTCpN|`P*xOj3}0Gn;+3L06d!t>F#*R!4^>Y&3xVKIOAx{iJdzSe%8)|~8-1`0`DH=K9XjslD88Zpi3L2F4|SNn|(yA<>j@F-XhdSmJ;z<O<`bO6gEd+CnyaM8AYZa6=JYJr5EwFGDg_yfU#)v_og`nM?bdwMK3s9RRVm@tf}<ZocDyBRc3zmUP#3(r3!sVaz$>l&5d@hW^rBY#PO$iel4Aj5|qF!Z=QxRW|-Z-KWg`(33N`fy~_SlmJw6O3ZV(>=vV{WEdH8qnkMImyC;ifzLV*kCQNR#=YUt+M3P&nS`I4YU&YC8$$db!R<8-k+lYXxu8nCf-uaX~2qrsmE24r{6310ymAt<zP7Rl+ibLo60<Aqel<u3ELm10t(B77w{k6o+W}q(6Ed5C<m*DY%5=wdS9ux-vJ1bOKMIA?X7iM>++N?d&b-^Y*XtvP5n!w=9J2w%W^ktyN>#~o79+jBg}B)(qRI_38<(5a?qd;GgP6$08%BY%-d`DajBsI5T13QcL%c#P5|V72reU4CPj3?)L6Y);dk(ACa;K0Tn5~S41x;B6!N@`;giRr{iftgj?=L1&Sn{w3Zf2rk9vXB{u90~cp%u?5?ItpMS}<6tU<BB(~z?gxI6_Y<Vz%54fq~-F8EsA9|t-MGW5mx(!WQh;-(eRl}@La_G{aE17aUq8vqr%EO@pg1e-j>5-?Nn@Odg*y3UT9bmLY>{p%U>wu!%h&a==+v8fc4gHsJr=IzX7=7AMnifr#|&T`RNsXD8fTV0>tMaglIEBT<3%Q^;O4CGBws{2!)5V|0yuP(P&3z#kVZ311pa&i;;JYc?A^)8ic7Ee*FJHB6mL!6Th@&=6*OzAoNMA0#9L#CvT3&F8NeaL0}s-O-YSVVzg(1(BWXI`2UGDH{Iqc7hoYwgtp&K;iUIX@3Zxt{Xmv~>*lq2vN5xWU;g2DiWiSm1k|{W>`*Gj}9R&z~NSEJmgcRb1YxON)1Q>8i<57El?OqL3$`3p=ip!d|PM5FNeqyn)FWU8mo}3(43X_}2q~N@!&8I7lyHDs;8}%*-8-0#Mv*2xXWuaR({r2Z}9O^+X(oHevD~v*ftYsv(G1n5!hUhY^Ku0Srp>Q1oU97)TAwVmD9SFS^Gn=uDrK6{Dx{VIgjet)m9ZM--m!+b@Jve<1S2fE0DX&G)4XgL8)U<Zd)>nG!Ss^UB#O2UBc9;sKZs0~w-EaD%Nz(m8trIea@+120YOawqH8Gj}s#H6<JJA_N1Nqvruwr?U*iQd@TI#@$Z{ew7A{0mF6>O(#p%yeDFM0vn1O?z~FFbC|<&4uu)mCAgo#w>tC5I4+U_9#bH1Z$MuCk1fNPmYox>C<hvSONEtDf8N<Hf`gTVe2$atd_%xK%tkY$oL38urgV^&mdcRP2ywCFYfQ^BpBdBr1CgnvsksYtN-?n&hH7-v{D5eNBUUUv4&D<#l~4n^i(<3AT&I~&u?{~`-{B1?qF(#RS>M+nVZzjeF0@aAz2GWajRs2=Xrh-rhd&S@s?NKbn!HiZecYH?jLG{NZV2F#b}7WcHJlYl3BteujX9+)oY^LNACmg$F$duj`0XNy&6qQEn82VpzW~W7UXla|S#LHA&x0(a0NJGgps1W$jTajERBxvb0mgI$ebEd;GzD~&9KK|K;|{&6QorQwm?&Jy1>MmX7GQd@7;1$jIild@NkgBS#eYK5B%1OwLM10a&b2ftZy>gyxiwlg#fIo*v!KZh1wlZH8<Ic4z5I%Oh=V_}^m*;sMBIu*9}g_f%ox@+_mam%g-O=GH269$>d`&(sS*2wx!8Zt42ro@hOnizw_Z3WrxZ+_)KR5ro)RP&Qs8u(m=<7kg2?a|jI{DS{1zlk0l9+tdh4$Tb1uwT197Lf>5m)w+}zTn1=@<M2(ra=K<B4lXg<h^9Q3MU0txQ0hHQuP(Wdbn3@F?{RI`{ct@wi(yt1U2fwW|{&Y-q<nU+%Go%?&6(7!E4;>O@&+z7^lf^(c>S;aYI5ufwG`)2(2=!#51$bf|))N0PlY=;HceA*69CzqCaPE0yMwOurSN|HPHrAopJx_JZ~^~~p~viT&2l(B%&F{Cs32dSBk%7tu&lcXSms&$ex3cXCou*S?M#*7{vm65cY8Fn}gvVI2eg?Z_Q$SNUNE+sKxLoBm`{#%iEGZaTB3XZ5yV$dXv2JASYVw2*HWB}(}w6@7-GNSA}ooy+&MU*TmKW7xVMhJxu>SNIIK6MhJf+|G1UVI=jHy0b$=Oc4Vu{$P2N7sMjg-IO()NCX+WIQzt1?WYZYPb47iSJ3i41Y8ibO7S0{|b^*$t|FmJ|^0$%S>n;#=XO+JB>8{jgF?WhpO$uq)xu!JWmk2$kHd9{B@74XFLYh)ww;`<{T1zFSA}w>*h<f4Tx?aB+7oRAoYS!RzWW(LFg360^G#>z6>}4AZV`CexC7guYl)w8suXkK$tNWAtRE$0bw!bY{%23wS<4^9n=S#a(8~vT#TZTK8S+z=(;W2A3)1B$r_7ww@g#ZBEZ?$?{K&t?y{ZQ3zlud?2|6VwAmpp-8*-3AWkQhR};u|yG0J2g)@qnQBmu#QZY)oWfP_Dbw{^;B_dm&0=!K?l=Ru7`qI!-bM9$(1$Upx?2+#DYSP&&kk>+aq=LAg);$2|ukQoE<+{#N)u1MxoI14}qRdpD2FhBYy-}d_w2I?`8IS2!d}(+QOjDd}p-D@PFwY-rqTNw1wz@13x|M{J%CI;NSi@Jh4UBl-RPF%XUL>HD2#HSBTzCk}d}vxvx=Gfxn|u<Jw(X$Lz>n7UoP!4CN@1d@a(g>ZQ@bseA(urqiu!F_QjM&=^yLhl>T^?(O`#VYHRoyAW3}?3DGS2A{zSkZe(wDJ0Z83NT_SO|La`e_AF(p#ckLQ(f2!!!phZu|q~v3PefhQ+hiEM-mBc}J6Kd`8mPolN<qE5y;oq^U02Lcu0u|_1vvpdh%-l&6wMNJ&eOy15@zG^?rotc?E0U_F1#T?**svxdF_;#>qM60H`-}76$Z0}w0|F$jm)iUMPw6{c2D0G1HgWob?C!U71yRYoRGn8q-3;AUlvuzqnbx#1O=qs2rc}`Nw$fvwLdJGBkHF!w0#)CIqT>0idJ>o+ZXUGl8WOVs%ZI=U`LxF<iYYl*%6hr|yufaS^tTkK;kfAsDtNx^oRz%5=7vol5ar8u@9e&MAxgWu062$MU%=xQTeW2rj*8xt#WOYw*ObmOx7`=!BiRlx_Ne4~M`gkw4>%DwE&Z`Eu>`-&_q-oMWEA#B>v2CsSu31?l(~=UkE2F>($XW*i8$bXGb&~8@+}W$W+GFdZnFmc^o|~j#s|%L<F1O#C&#SD1^Cco|0Mnx>=YeEh83*R32^q@Vg&*qL*pcPrS0e8xcvy8QLQ82SZsKYkTH1Z!ul-(HWgL`2&?}aQ@13(2wCmj4aS9nYYQ!LeJo%=&mAI1DFiCWQAq6oiKkQnn|jty8TobVv!^>Ac|03Okp57Yx&YWHt&g<M)&`tbZ15%`I-W$WOO-HO&HHn#zM#$m-cBK)gx&1>?0JGrZ^PQ}=ueIQaXkV^CKgi?taO)yv+yq?*q`F%p8(X!>+EOG>W;Z!Oqvr0Zh8M>J)&qA;MG+c4U5<<BAG0OxQLA3RTZ-REY-6R^4^Vlw@TAtRk+=xhJ0yd#~VyYayw)_MH#PbQaeP*6ujNt_WzePju_GSoH4IQ6+Jk#Rsf0Z?tY*M<MtSM<e-O3(82A4n>;STZ;~(PxqIuEBt`7%G7{|@;;M}_G^9Ga8(OQLa9-^oHm)6djGHTjms#@q2sIEZAaByNZ|2})f^>M!d<MZmRi)`%;>75H5l2d3R*&-Hyo{YUZXwqrv;fi~JrxgcYV?OJcgb(Sbe0(fhDA(tlb9mq(j5>hfT(5_cAlon)u!`H8h5`&E4{R33ig41Ch-t2%g%8V0u}C-Tq5GoZ1X2Ar0tBMw%~V;jv%3@nF=}q-jid8E1)FVd-@#w5B<;B9H`>bgPDhnkQTHN@&)=w^M3LQ+3xZ-tIjVkT@kRhvx}zzKUoodbTJkmF#1PL$qcUD1R$i*jJqHKC3)vuVu(-TZBx}#yOuyo3i*dOHB9{TRR>dbDb)y2&VFW#ryd-6DH9N{_=~nfEx5s(MzB^!mm>hXoLJcB{RfmH#6H)0ciLT)>2DY37h-p#6N}b@6^Y4tyezzKI^SKhC5e`W%0rkFKn8OP^v<xZ3`=gne{n>gH@-2KeixYzB?ZA>H33M9T5^>%PFX_)1CHltsl;xe0BFxyFb`cj1)zm+%Pp3AO$J_?=8EL_oF#sBR&mL=>9`F>xh!#SxwQA70#{3olA@ey2(JbB<uGPgF;i7)$2K}Z>KLzZm8>t0shYq%3mk1HMeR@ke1+GX=h#qAv2%x!3F6NyH@+l)dG74zX|z%jI-I}(^?rWPy$8d;(t9c>wAI9>?v*@tAUnqglpb390eot3g<cB@O2o%C$!r2VCY{j44nSJ2PAHr7sF$W`-1eG};TLHlS<}ZR77Sx*Hb5t<uMS6IieexDImQKPyw`(+J=Sa--i+I6gmG4yp0;gEc&DAl=#5_mJiOiz^NcU4tTWh9?i|~+Hm+df)C*E=Wk3ttyNv0x^N`v~-9B=wG>dnzY>Le&W3J#?>uwh|k}ZOl0F@C}$g2qme9rRD+caZfA&(dN8Q9xtJ+A*6SMuw{D3T42V$TdC{s>d+C3kawPp?eig*&DKvmjUClY%grRF#~UX{YTk3A$Lyt99CagBHe09L)QQ0Ee|5x}1+oLr}a3Za-<G!&XIWasC7PV>NBCbHU8LQQkIrV?Z&XLO(zH0Z*%z?8?H5vm1%XTs63y%Mx7mPmfoSk-$gy`8wOD9A(6ehi{`qYq1`}kaG&5!U;dGAg+|slsJnkqBc1z2ME(wi=qjkejs)eN5?wAR^8us?Q1Z}qDx1AgQOFfyxUbG-~yyZS)|N&T#_Pb4_(I9U}mWh5XE)0^#g*ec%TKVHJJ1O##&3ev2W`WtMcWAj^m4Gb1if>(p01)Rso;ptlDHXN&PiMlV$8&f<RhDpTt_l#Fkm-?Ewqe*z3j{PC}xK!Z;T(Lz=M+MJJ05TG-B}v8>?!d_it@+gOMrZD%M@neQ4_qZTlWjl|-LZcgl8%a;R&rAWm=m`7L~DrF#M`}1%)sQ88s&6`6WO{0L&FkE$htTKm#2}A3sPH{p7Vr-oSI*w;TTKnlHV-3(2At&e_)?m-G$jrBn&)YvFdDjYU%oD1+YqVe2vEO<PBp$Nh;jMe9^+|;{1Pn`?v74bFZapu123B+YuG!9QxZQy?<n{G1-oWDHK|QW&U1G%!YL4EcdDjlv%~LFx4I;7Jd8>vMDH;S?$A@CoD_HCYy-JmO6Uyy~WnkmC<hidvX25bP^nhnJSqBR}tCQDt(QRM#?(|nz$h#y}faYdkL$7%^Ln043q((kfoze^PJlNTIy>r`P7Q5S!-vyMt9^^!Cc(*Ye#L9jeQ?9_BH#?Io)JdvH!C!p?9Al5hezl9SUma#1M~XX`q@J93r+2hqcHyh0$~6_&=#aYh*<w45jdmO03mFVoQ~=$In!9ZwUYOTga1u$@8lA`9J*fk~`*N@L*n;98MmirzyKiW#E+mv5UiZ%3`j$_Qo;$mz)VW|s{ejoaUFb#KuMX4NODrDNO^8|q0TRh7R#o$L(Tg6^Ux<ROz4E2={<-r@M!hYxFN7WFQWdZ~mIw!>2O&1{m;yVMBC*TZ(uIc^ds*P1Y0kxwLN%;m8B?>a{J+v($y6cKEi;AHe9m`U?z;gb+DKAGV_lY*BBs;m0_-GhfT8%Jw^@f1y}lSlowV4p?+a*@t9fO&Un72CT&5NvqhLnzIfT_^2tYir(Q_4V($4;ecJ4rcrbyaoXw0-(o1XnlB@njsu)I(w3p?B1dcj+TQ9-EP{2ku)Lics8i~G7ZJh8Z7SoaM@-3n#6f^0WsyjzVIier~xJN_OA=GWC{e7$qJSdgR6&Ff7QxhDTZgGYR^=)Lv>Wa8bb3BJ{hn^R8|L6|k5q3+}kx#Q6U4<@*&a{GG-&3x{l_?xv(11+e0kQ8jMpP}n;*7xc0B&=xCwhVA&qWpGp*rl?|`WxZFULR~vNaI=;{c`&n>Hbm16q$Kau*LSOi{kQy3U<AVf?fB!rO}H{n2Mcn5_|Q!2I&^#(et9(u+vZOfiTb#h#qU3B$w|=l-Ij~wv{SO(MhG<+NN|i$#)8QtInqYs^ZK2w(7mip$nZ$30RFZ6STW5OEKx%Dev2K&y2e@Dn*wWza`K+uO|OmKQ~EXk8(nVa_cyY<qae#Uf0kL)*C|griKppT~)iz_)ey~kO)XTMs3Tj8oG3-vsu>Y`!@<bLiy|A3LiXaPfd?+0igU~nspJxyintBbkX=5f%NaeEZ`1n)QsLX<Lpmw385ROw!hQ(DFknQ-OC*z^T3+_sQJ`jFDMx>#vmy+6mK|Sgjx4v0yXiFM7vmZ`@YW0fIJ-=Pv(IG;T?5{Qs1unJrBWR-Dj@wZamgMZCd&_iX+;z=RR=0!Bur%?x2oIt_^waSvWnJ!D<>q&wZagW7;!6^fWSe$9&fRjk!p-X>wGhB4STGBD&?gqJf?ts1U-LL}Yn;;4YpW7uY)J)>jg$T!v-zTgK#QjO*2~X(@`9fx@Av){3x;Z?$kLyPdaT_~y#!G<tZqhuN|>FN|WVm9;bynTZemabZr6(pCdizbQ5$BML^|KWLCEfS^yMw;E70u}icXSf^!Kd>O@IkF<?qe&fb}EP|(tjSLKa*8Gs}WO$yPUs1n4f}Qi{9ai9UdUh$w;#0ASH5mAt19i$ZHpCv+AfjW3z!A=!)TKse(I}aL;jxXL1I3NuutOjm&$H8dZYsR>iNgA@s)Ku26W<S%Mat8qqm+HP?yVnpu)56$5|ILHl1F7pLE3&mN{v7Xw1)+TMnWfb#!If~m@BM3v5T4YK&4z55pT*7@!yT;G(Q|9aBj}4opw3{v4*`ypih!asz42jRzv{2rk%HGkT@t7KZ(#?UkAamrD2_y1@h@EXt+He?DI}tpx4FIAE64!7k%FxRhG71QNj~}`QB0RbuoPxK5=3}pE8scZq|z$Y|-y2LAt3n=n`w<v6Hl`1@KY6Ea~r$AKEKras;tHLzR8=EkeXyWovcosLqbGa6(J-j>@)9nqf`?LhNa#y^~iYi0)I^JAtxU>PNgfVEg-qR0jl$I6eTcM^m5|^ks3CWRKC~W_XT_N9In-Zq1b)g!L=8%IdM_ik}vv=X3ki{r;@G&eeR{c*R&^o*wn;2yb>t5h(-BUnK|1-QLaP2?T*>`FrV8Ol1a5E2=o;+qpDmMgC-<hMSi1tpi=bG3Tu~Iged7paVrbf3-uqR3snn5whLSDDlb!%k^9(?6kXF*v+V1-ox3*)GYm7^?r}_3{wi5c53d|du{Yp4mD^-XCl_Ta<I>Ed4=Y$#7y!tT9B19yJOIH=@C=$Zb|eF)I9%g5#KkA=}}PmK{FDS-!;IMqT_w@-MfI*Lzp<gxM|KSjyQ2gOk-B?xKyx_w#TvX6tU_cRp~oV`a&UShc{=T9e}q$;%6s;XH1nf{EJqKVjR>J9dgn!c{(tsCLoEX9Zz@+qDS%0>ejqIrKpv*b0276LtnXGb@qPZn2@tD9=RfRH2d-;PTn4`LZs0kHAQol0}8Dul-=O)y5ZHA{fwN(T2y;j5J#R@B*~o?VEXNRj**(a6`{)fC8fybu&`c9v}y&fKO48z<t+U#WOJ9o-*rmK9=yJr4lq4EXhAo|4iGI_Em9y}JLHF_1^o7kHvY2LuCQ`Fpm)VPmck_`*J;n{NF4J=H&ky=^}Ql3pQKjES}*9Hp5rD$gswKE>S?V;3anpl1z$lXv(}wm;vLf-LHSvd99F#ssL`O?$X}6z#$8EcE3Eepnr^gVXPD3$N~ig<Ynq)*;?e->`OdSIRZT4c599B;;@AO;MLzD&$4FGt?d2vv=t|DqrpPYMow7Myl__q~C-5T)-kB(HLgIV)1Wn@kF*bd@|3tr9mpU7Ekl{xcfey8j0Ih1Tono`BREZDzK?+NKJ%Q@xlDl)pABQ2R#Nz#b(&r3)M2~xYkg99$i7NT9Bhn7FvfHzqJf>L4-V}05uYA^^CbC^d&X1prVF$SJI6Tr9lIp3ZGh*q{s0=M(bl!36@il>ht@3@Ed9qv}l}-LGP2QQuyF(~rp%mb_xfnODUGGfJFG1zSkk`uKOaH{P629WrE1SOdiyx~ihjoMpo1HLUOmto=#XH#B%QfUnK-~l~HPDkNb991la>+`!)tWbWsoq@GO%9LTKE4U;F%Es<ZKvt0y|oYX>b~lH)fYsC)4$k}=2oWo8u)Ij-fAff8|WPC(q^`jZ?A&Ys`DhJIQ~z)Vj<5|<=6BzWoVvxW*vFyHBykS;wozmtjKN2I_Cd&0_&Kq8g<L0o+NLwD*76~Ku__LW`UFwexbNoPxFJ;{vqKLVpEYIyGD0gUmDac&&=pKac~9m3o+!hA)^2h2rsJv(1NynY*Rp!klt^OId1L0Toyq-BLPEO`ZM|c^$HGZczkH$j`pyBa%f!B{<i<;>EDbzxOaQ#{`iC2w}-|iCng_^58WJoL~naUZ+kR0es^%_+pl24PUQ`+c!1(-n%4Wb|F-`X=)uH;+x^<ugE0;N3m+VBdjz-nNB*e+iIB5v^Vf7C+UW7?Z0LJKqYv))-yXVPX!kbX(D-_12>T5zgeBU`)$nBtUuFXj_TL{Ix`z+)KnzU&t6o@v$<eDfaJn~ceEB7PfY0OM754cTaNm{dVfW#c&VASZIqW{X;@%fF<u5Mv4~+L~{J*R0AztH*@6#_X4gIeF{sh1ApZJYAB;Ng>eR1jbc>m<x`*-OVudv&2r@uSr54*x{o9MrPd*aUc(8JEt@c%jifE7c8-V?w5_S^pjmm2lk"""

def replace_block(src, label, body):
    pat = re.compile(r"(?ms)^(" + re.escape(label) + r":[^\n]*\n)(.*?^\tdone\n?)")
    m = pat.search(src)
    if not m:
        raise RuntimeError(f"missing text label: {label}")
    replacement = m.group(1) + body
    if not replacement.endswith("\n"):
        replacement += "\n"
    return src[:m.start()] + replacement + src[m.end():]

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ".")
    payload = json.loads(zlib.decompress(base64.b85decode(DATA)).decode("utf-8"))
    changed = []

    for rel, blocks in payload["repls"].items():
        p = root / rel
        src = p.read_text(encoding="utf-8")
        old = src
        for label, body in blocks.items():
            src = replace_block(src, label, body)
        if src != old:
            p.write_text(src, encoding="utf-8")
            changed.append(rel)

    for rel, pairs in payload["raw"].items():
        p = root / rel
        src = p.read_text(encoding="utf-8")
        old = src
        for before, after in pairs.items():
            src = src.replace('"' + before + '"', '"' + after + '"')
        if src != old:
            p.write_text(src, encoding="utf-8")
            if rel not in changed:
                changed.append(rel)

    p = root / "data/maps/scripts.asm"
    src = p.read_text(encoding="utf-8")
    old = src
    src = src.replace('\n/*\nSECTION "Map Scripts 22", ROMX',
                      '\nSECTION "Map Scripts 22", ROMX', 1)
    if '\n/*\nSECTION "Map Scripts 23", ROMX' not in src:
        src = src.replace('\n\nSECTION "Map Scripts 23", ROMX',
                          '\n\n/*\nSECTION "Map Scripts 23", ROMX', 1)
    if src != old:
        p.write_text(src, encoding="utf-8")
        changed.append("data/maps/scripts.asm")

    p = root / "layout.link"
    src = p.read_text(encoding="utf-8")
    old = src
    src = src.replace('; ROMX $57\n; \t"Map Scripts 22"',
                      'ROMX $57\n\t"Map Scripts 22"', 1)
    if src != old:
        p.write_text(src, encoding="utf-8")
        changed.append("layout.link")

    index = root / "tools/recovery/bank57_source_index.txt"
    if index.exists():
        index.unlink()
        changed.append("tools/recovery/bank57_source_index.txt")

    print("Bank $57: %d file(s) changed; 134 verified text labels + 16 raw menu strings." % len(changed))
    for rel in changed:
        print(" -", rel)

if __name__ == "__main__":
    main()
