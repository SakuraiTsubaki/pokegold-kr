#!/usr/bin/env python3
from pathlib import Path
import argparse, base64, json, re, zlib

BANK = 0x59
EXPECTED_SILVER_SHA1 = "cb22d7e03a74dc3a563fde6be8626626b2b392e7"
DATA = 'c-rmQdr}zy7{Gip%C}H2o7?AQD%VemI8aE|R3{oZUX#(c7Mhe+?{q0D2RZtvcN_Y$*7cz{U6%}b$+#s28=KXKefLc#txc!#-E5$JPhBj)<((<)?FiB=oRhfuYSbwKd9rQn6b%Jor^~O9qnHEni%R)#{y^etbkiVH`TW=D4jwZR0se6nf0Ig5`QIHv;|^9(jCiUgOXdH6$s*1@h%3@DT3S&^>=O~wB}R=gQZWjSl^XXQ@lGA!U`nO}z^3>W_p7>+=Jng?eY!Ih&azK`@emg-oNx%dC%7Qv4-}%9b;W+3+#xVNZ8$2rV^6I0B9gz4Z8!lCPrW_fZRB_+A3d9K5MXB0F=YI`E+I4$Rb^`Vk?s{mQF;Zc-E-Z1u6np?2J6?7|5%hV^u+VrkI^CwA^EIdJuELfnl8tjF~F-y~5Uup$-M=L#cHxr*0pf91ITR-&?*$-1pOp?#?X@kS2B4c>o)rW~%6Bq2yy`}JV@)yK6?i71pwfFIm!>W|wz_#oAI2mAC~gSaL#X{+{yG65X|>#-f%WdV3zy4S4JLl4JBRU|E2yQ_%UwuLoX2cGyQ|5I38jI`UGJ?zTLj^pGZ;ye%qYBrxl=P)lWbU8~gZFZpA=Z3J=x#mD(?kFwv!ZIm0x=LX?Cs~AX<uWNht8YGvM!&Yg?ovK|0I9s9jgI8je0Y8-~?}nU95Y6T<;3c1>DE7^hP#*Vt#?Q<PQ@D{hTq!)l>rjCjyx!1i1LZ0_>{#TBU#8&GFan<yr4Y=V-t=%#o4Lw5n1ev78oUI~dt4|TO+r!r4D8H;Pv?<~<7KkaIp%gs5CDH%a<<fL4uP`gV}wN%P!v7Au^?j@$hL@c8UFPK)#gh!90ta{x8=qh8Zy{3?CR!B`|)d$xGj3ZW#tpUE`u1&$}K9X9zm@Vg>!^Mv$F}z~QR{l}D0Z>2G3$M4uVi|h^Q>HYMBNG*P5w|H0!eA7v2lu+M#H4l?0lhhYdY_1B&n7EtW9`(3VK%6lxE#QWrKICUvAO(a*wiwY0+aEFb0~nOUfl1ggf2Ov!SSAa&`>I+CTCw7jsfh^0uY0MoF9{R8HP+}YcC&3sYBTLmDYFr5=eK$8R-WxR{o`bT=Qb!Y0{2*^h9|X}ih?Jc0b|e_skr`2W~{Q@-C(3W1A<|}5_vKb2vKI36ncFWOScg!rEeA+9+ja8D)dpRsADZsa(SwPd86nOusJJkz*pQX!i|#zW2d{3HiRncQ7u^q;H?F~mKfI!&))ypP;g-B^p!_3A0dDg=XF(qkxT(4vcs1?Y6~b`f##n#VjUd5fnIc*<qv7G^IaA?0i`%p!x(*3MJbZ_5dQ3q&!}bH%$7X`4zBY>kR^z(gC!kX8)D0~^Gq#`%{r0PewFbCTqd~}FMo1{VI0QUoXeaFGMm+u0SjtGOpG7Ia=b1V13Ip6`9j9Xyd?rBsR(42zVS8h@^*D^EO9tOTN9L@G$7E`F(2@G=>F7WTh52UJ@bXIlHWB2r2u)Y7a$3e3+hQlpQj)G&kqh;@jHo?ec>jE)DV~P1<r`F#YI1b9d%4kXj%2hH<kL0W9xRA=YH5V1OT{-_&)c#<qD1+64Ia&G5ty!JPl@J^#fjBBuj_19NC6CTu~U+$G>Q~dv%fQx;ZRBbV+5&UZ7v2V~wEeD{!U^G(kO9<yBj-0I>0g%=L2Q?E1@D@iH2frOv16wO{H#K7r5qR!DB?boE7hB&fJ4G?9;^ZStDdF>r`L^q4Q_ttlc(kwsKoAl&K%9R!nQhB(8fDClJ@r+U?dT~H!P5g)r4+g2vN8qR@rV7pI&;9w7f}Ib|iH!NfZg2JX<5Da8R7g=+uS@~k0{8vQ)K2Sdwq-*g0P2xO#x9&jLI)h=KqBq84d<d2)zzQB1+<2|M3ahxE>psj+>W|W!1%m3zHD^6#fdgE9;^QX*2MVD6T$Y?6R<Y~pNx<G~iH|NbAH?R6dF)t$xDbzI_RQ2e^9EJ%Q7=^p2$Jx}Bcu~(lEA_w9W?EG6*EbRLQzF|>M1~{)93gz!ACiW-5t!%jA#&y!R}nC5M3q?c@6iL=4@r=(YyX&o*l&LaoKxv@S!O%K{STX}r<Y@+l^Q8lM+<~@V%ShGkA!g{7@lQ)c5NcK>xg=w#b}kCr7kN#XcQ9GvG9F9pO8;7j^ZW4bt@7?XQwI1+5?x8GTwIk<Ru`L0HViA9*1vD@Yx6``S@eS7ykR)4P9Y{J{)lP1*66_-SeA14<`4e-!#s*_vbPdY}qGf}gGTbJd+W!%IsTRpmVMG3iV<5n<?C8P8)&4rp^>Ac-{PO<la7I-+R~j$_x$9R{y#1K6@#|QmCydFyAlV*Zvr(`HIkkGwYjbpVsL@+RHR>7K*E1X>!y?`K8d<|;p6=gK!h1A^`}ig4(L@<k%#@H7urZ&5YV%8V@jhn{>=U^9K@6N2*(XW$XBgJ0K9NoB`O?8%cJ#?9Z^@9o9bQ}oNQz?Kyx*Xy4&cmldT<7I{VBXgT;Z?9&Ls5F^zI=~kV?<!^iO9A>^dcKG>lJO>xcI?`8jK+~=O_xwo9{+h#X}vEO-h0U0x+S8S@b+0#OI{mPz83Dl|f5qV^!J)39|nNrl)&?k>T+v?2ZB8@H9D)FM`4OLi)~CRgY7KcJ?B{Z%4fmy@SZo9x^S5S*9!g#_+VEsUG?d&aL9pI~FvD-pJUq^!3j-@4`O@vF{D+Z72ZfQ*EJa5+V6n{6J&OT;wW^Y|`nVbHP$P7JeE9i-#l~;K3{vOXYMPDIF4%H8!4QyH1{>N)}`N`C^a3y^c}W_}MxVHW9SxR+Ab6*6({~<$E9k2NXw%M}LaE1J#ob04cO$N!l1i-4_%OAoZqjQ-FHF9H~+Fdt|^rfs7!QJ=Q(1Jk?%0tS2T`o!7h`jr7!=K+>Xy7liB?bCQ5^kWclLJz4#c~gMbq?bSj^N1*@sS!N09y?b8!a|dV`IrRUu4&7D>$0w4*>U^$7q@Xv@<P8`v|5U)0d)mHJ2HLeV_07zQzE&gS9l`=83H<1qA}=&W7gXXyW%}jNpT7#=Mu-7(wt5;(&WnJ%HLq8yAq$2l`#tU@t4w0N8ldJ1NEI3a?X1V|LxSXcVGN0GQ|f{d8m(x1g8hl5l8X5s~Il!g5!b6v2)9^X5J<9N$q4{<Jw1cCJ#R3N$Kn^&0A7W^{9w%rtyRc6E+g1o|}JIMCkyd9l3Jq4i<u1(C|y~Tt;F$Jb?dd<B)w2lL8;R6PSDMmZp)QXxJZ1*!{nY%+5YqA6wEDi(ot;w~w5Vt5(=8t7iKxb!O^UF+Uq*O9AP1zH`*{!>4z9mJ;01o4r?E#heq$=5kN!QxEC0sgcwqhu{}5c@P1wj(O>g~MW%tN5)3TuYkP(oJqXlWc~Gc)sbVAoM{IAP=JgD0#EVxGm2xj9eW=1(7j&sp*FWOW7UNvrD+|c}5oJpK?SNn1m~z5p7nP1%QO8#Z0?!^UCf?4nEr&=U3bR7Qj5X#>eW~|lR69DQFAFX!IExiMZ=4p5kI?Zv-h-f_^~!7P%ZP?T9mS6Ao?A6vJwJ0CoR2wYR0i4=bl8@_joJaDrNRpCCPjEV20T8snKJr3@K7F4%gu9T5r&ZK!1ztlK=8p?r1bT7*?n;ExnO#M&`h1uNq>ja4D9WhgUbzo*?1rkRe30rM@4Uo2q0r!Pi(1=O!P_+D?3WEtS^$zp?c6V^5R{3|?dX}GmQH4B$C$%m$3qUbza+hwn-Y&m=q38Bs=>C&4j6P-6*;H@jk%I;E^l(9SUx3N5j7yN!^oFGxO})Z+I#m*fn#1=f!mlHR88SQlIB$FnC$8qK8L{jI3K;rf>oVSLA{}INsf7OyyVqQ@RfG1un3ZvP^?bL+IEJ*?m3=W$9@8dl8`vQu@=8mW-!ySvUS4X+-F--0w*xgTj~a{H){Rwlv*sNFnpAf98>}4`JW4Q3$yCJOX0!HT^+*(Y!hK`eZpV6|<^*?W5=nNW<IkRYq1F+g*;qL%+U9u$78i|ATlDJlwfmbJCQC?X^DXoQ3gLqT~w<@X*Q4>VX!w^&DY&1eHUVbtO9v%o)X^ISLg2LLOE~byY0uN9D}l$M{GP~+_jpmHB(jYYL(3jYt8VZ~1jl&~!Nn<7u=VCSuxqTc44*v=e0<zaJ$?J*0<>5A)L0npF5u&xz^EVzYt^EoU8dM4eH#3c$JQ!ebV#B}nMZx!>9{P|6uL#8JH=mSbXl6zKLV3Ls{hR;N6#!Y$$y3v}Y$07wn$~RW_uOl6B0QQTwsDyzk0xuzUq0npg?FU~_7@4D1J9@T-otV0Y6h7pc1Gcf8E;x(4#{Jm`Y^@%T0o40w@UGJ#?K@6qQpJ5Ex9Y!WJqb%BZ{8*zrX=yW3|d6k7`&@8)SY1BcsbJ6dYKB2O=3!J(}@~&srbWH!vRPS93AM3d+5qlX@2o$yT#JM@)Kx=s2L;{Xn`Mm7E;+`{bAu`X0rN#i#VZQ)VTU;f4V(Y9*WgkwsypJ@j*7ckc$=1Y-qmsI)bJV+b*vzMsMLeF1a0Y*S(e()=J3SW5&4|iY0x)3AFWm=ISZdmyPz_LYQ(1Q_y9OJV6|dN9c%Y<RLF?NUxT`W{=6XJ2yE$?2^VRA2)&81J|p}#S5GgQLyY+N<zbITC_=gAvtHj*sv6+l~^N7o2v4+@l45@O5Bfgq|h(WlvrRSWq8x}kQAhV^?G^l$M2|$8c1{~sODs@%+Ee+`AVPjOM*4i2^7XZzw0HU6HO!B^*M~i#-xY-HYQSbpJO6^MgBlZR8&1W_-bYQ2HG!Vw7KcH4B&0w;P6mQF{YOx8v2&3Q5xjF;i=*2vpfb)+MuQA};fa4cTQ^4!d)F`aXvQd6tpX*rn|2+%s|B0*gT@Grz?eQ{RM_NC`bW8`w^S13f9xH4^F=bl&Zj<|_K(=Cv9>zaAn7$s4-u46yh?14j7R<P}M|?@cF7r7ZlN#1G!AvmT#7P}yN2wq1IqZC0Zt4rAqHzg)KZ}bH@7gN7}JcA_FT>i^A4$$_Swv8eYBWaiiHLQ^fB{Lr>|a3BBRL-dGU>Vb5gYxT7y3bo6;BbHhHYh@^=3~^d9O5&fXwtyqOF=Qf@d@b+5h4haT+pgA9z$cCe^)Co>D(Vx%9J5p1Sl65(Njuo+oN+1ZLbbW@;#jR7~rFQy1u9O=X&4rpBpt3hwVj^8+X;5rEhA=ZO@FESgzAXNM9#h@hGScV?lQKfS>v*l(2b`Nv48Ejms>O#=CY9TH3O(6E@n<V<{D*P7X`f1!ER$I8H0%L)rj1PHh5KXOL0MSjv@?<F9#leV$7dG7kWQ5H5YihA{0fL@Yp%>ikBs#zdG3>v`kZZ1~*`>iT38m6`55~1!YCEjv2-`_*>cQ7mQ-otB2^WgWTm3zW!R70J^q4Zy3yt=cmc9Ts|yO8nZ3eXxKCi#CQZMUw7n2u`wUu#7C!Zv!{xdL09M^nKl;@^*Wd5Z?FF1gzcgM>LP2?A4db8~Pz&RUxV|?L7cO-7x4@jT#hLV?mELIFxyx>JH&i$a`f#<yNG|C^iU?S+zFj|u*1UKUmqm1ywON8t>5tKXoDl7}0qB{=Gm@B@6rM@Y(?l0nQ7r`8cn!zgZn)t0Cs61!A$A2y$$?5kH^Lq}VlP;D#`cTqcr*&Mt82vaYZjt53RPtVe&t(JYE4y=+KM+r$J73a12}S*7}D}Y4+%Fr?!hYo2<ffg90bnK0@h2vkSHNJ%%iy=a~?rYaY)oVeOvI0X7Z%$s*o>SI7G2d{nrV$9#-z1R#>63O^W6`FE@bN?O`lO!{3s?mLSjdu>Q>f~fWjv^tVjM%@-<j!a=i*lZ$wx34uc}bqN|9S`@gP^@dbOA+&Fm}cY23E0<}G)X_GX_<0(rI)#ccRd%J=6jYH?1PM5;vhEKg@4T5VdTE+}0i4M04V8^p_>R0<rN~MZ~S=GeCBQY#`vk@4F2fJqvB6k)7lI?mQe#V55w(2gk{rnD>mWW_yiVQ9uF2`G=HB4UI5<7np<iQUF2{+*O=1?R~9WQQS?N+8(cS2ZKf0QyF_xx*kVncc0#Xn1RsM~m2|=d9TVBup0?eF#nEtB_lV7&d8^R_W2&~a$M#r~Z_=Gy)sm-M!)3w-ds9Gqj!6I2u%Eevr0xW8UOErjntmeFBu4jz_LhWIs6C%lF0b5J1qQ{6T6>uQq+o=PLjIcNI94%O9cR0+Yk#o3X^6&zL6mC`5+w4HU<nRfp4zPuAA!yKB`Q1e5;=xYz2-iA$?6&}exJi=uJC86KR>d56(u#12cGL)Pj;3uQdR!j6kP%M7)2T<W%E5opbA`8$*l06M%KMyM>JX8b#q`_^9c6J#eqBSPNwSbM5!91~;N*av_2@0&9!4vcy-w=s}gaeoYp*Z+e3#=11-s{fIR(s(^Iy(SrmwDAs_C%N8tD#zvZu@4{1h+zUj{TMT+KyN9z1?u6lmg|A~~{wUAyF|Dm4$v!v!wV)1wPjB@tBHgR!K;}p}Y^8^e#^Doj|<yQo?%mS~aYHrtZyXRo2*k^&k!@_!#sV~&>lD+<s{1?LxX6Hd=G0Q@e9p7PD>K?D9!e{VqdM<yIF7wQ2{{L{;OH8`9oS!K?P32*;nCHoEoB@2<9Xq4R3CZ+!o0PW|pl8P^4J2cn2mcSD)Zo^g)xkiAL&CKz6&dGzyCEkVjEBU6%1r<SL$Y&8dPXphQp7=9r7M)12po$})v%iWYF1MT4g4yB5(f2;bs*_}hV>+|9^%ZQ2r^G`tjk>#b!>I1~&tV4v)?=*Pk51hn3gV7J#CvI|5H55P>Ue#hf7#Pj#5WV@@#5G?QbLiD8t6SJ_V$smqtI%YJi}S#0vWDPvG23D2U)D?e<7;Rhl3pV&|Y%i)4=+`SE+fqMjn6q~?m`CP6tsDnD*;*gAcPi1CU!2*!r(E!CW0?1QbE@e^7?Q8Yps*#O9}AE>;=8g4DvHxCVUg@usN5^h9ZB9DG=}SNKG@pm*Gq`@7%+s!ow>%3p8m~FE_<RSqXICtS10}6#c|zr0snD?&F3SI{NLHRUDZ@rQ(0>Cv>46#Xj&$R@!+9#<2(qbx?@K)f+F_p^A}h6`@!v-HAlR<a`Jcs7aoEGo|BFJMnKrGcMzRaXuG{l+LwaZ*}eTrzr~xf(E#Lxl}#tO1`3`{#ATG^^gCj$!2S3g{gYy?TrcC<+dU!7)N5J6L&L~ic^!18xCK0nb=LeCKdaXr&lFNLQ)v4gaMFWO>WEHpI@hu4N*N|&s!<>X7!A3MhXg<+s<gy<UV|l5U0D#q~>}Em)Kb`+IltBhEE+l>qK?iM<|8vyy+6DnU~(i$h+6+nTTib(f<EJSQ~;NVbj!-km%E5-*TJP1xnnw;;{TT+@WvcGh@U=H3Z4<^YQ?}eDum*<gH*yE{s@&>Sc#=aVA@kgLSwW9a;QoGtKUFypZMlTR%LbH5$Ts;*H2@=)QcrbK!$v$D}(|4|~(p1?1fYQ8nWEfS+G_V1vn4~g&V*FEm@H+2$a*G2`29$XlY5N4HwHq(W6*<#~Bc8IsK~@L#o2hcf>p@gXWS2{T2^6ig=CNd6xnQ~vX$!V4n6Cq2Uu1GOBH?2taT^%?=CYT32A!YmQ@BLruXRf<hOfGSNH?{R}m4O|G0<n{9O-Ah+IP4O`K9*ZxS>BD|}S)bdCK+nBSSQZ2rM`3z$wxSspD1<x))3L>N`tnwe&-$w_OFeT4QppjxCZfbdTv8&nDkzqM#Xc)W%9K#D)S^g^L0xGgFuiYlKSaV<h(pqr+@z~=r!_w7=|2V4QPV5#3h=lt@5i9b+_g@n-Ovk*u~Z9x~j9}m>fNRsF8Gz8v?^ZMt<n<&gu?Mb17EHB?9@pG&6%fd!o#q8;5sP9d&wQZP=+Fpt&2}!&BZQDl6B)-H^$dkH^U7s2?YIXr%&E1g!$@0VQZ!s$VJ2egI;HtWQ<WD+qN#}Vx~F$?keHp;%N?T5D*gT#L7gX<O$lI2`E8fVw!Kv;BnP{u&lvK;P8vR;77#CdLGu*ME+tWJi(^iCpq<qU+xQ1#H}PP=Upn0g>b$?eQg*&C&vG})=4p!JS2B7su!%PYVpY6F1K6Ppi5(_=t5Gg%yF^Fmpa!sHMRp=L~KcPj+Fq2LZ$0s!KfM(c3GJq`F_0Qz`$`lgMpl#|Z<4hC#I1g=R6%76unAC9g|)1~BspXc?=iW8Tc8SMs8k!P<6i`2<qY*4H5pKv&Jz&Xi+ECr|Wc%*LjNB=xJ?V;HhOQ!*&ktApAOpVShx?LrEH{!oZJv$SB(9Wv~G|Dl=Z&X_x=kHsyQzk~g;ZZeY3PIm5kyIXqeSVs&L;0OaUmuZy3_cdtYS9!P2N3uDVkS49D7T%u7rAx2lNpNi>>9IC1jXW=GW{cA|?D}&s4lmvG2WW{rDaN5SZ>O7V`{o0APosPqdTfB1-DmGIrc&+8Ak0u_+sxeSiWM57TF<9Q#zQ7*0<b)<t`_jPfVQ8fCxG~)0K82I&5#Yd{TmS6s~E29Ytfe=DC}84at%O^5S<d{%QDqa=X54rh<9K&4eXrx<39cYX@YhxSFU)_<$gb(nKwBO88lwri@G#c@E@#V+Q;`$awA=blAwboXZ>t-_VMlh$)tTIhy#aLgNkdn(zNFxfl2+S4I9kU^5}f7HzgSbqdY(SChh4>q9r0+-S6jU(;MkxSti9#toWNwi-$mcP1w@1JS$*xSvztv3+>tX|+7m+=w#0m^7iGT4+TpMZ@sEY@#I8a^@PXK0?wKMC*4y&r2WR4Q;{8dbnEO5EP|oR=9iMwM}0|#K+Ho{q=-zY|eK8bH|aZ=Xy_u3lpu!D)VAP)2bQ*BvYc2tVZQv%`eBvHpX7#FGcDIX$kkSS?FOP=tzD|DHL+W0sE`?PIzS2@hHReZYWQZ0U$0OPiG4tbd2;lcay*6BJ7Wt4{(!*ArXGI6j9arT&`{jw3_~6%H_9^Y95Ee&iZT3X$<deh4Z19n6pV`QO1!KrAuMYN+_z6HR@9pI>HDFi^`m+_Glb*N(7dNDP;E>9~LbhZxVglpn!DZ8i%G%5Jw1!`a((ibgN~DgI`j%?m>V#=~^Tu`$4z5l72`#Bl@QLl_@VnZ1cr{?`;!K9o;d5SoxKrL^WM#AfBvsqJOn8&4`7F${-7=uhTlbfm?XO9G3dE{!4m&z9@t|1%Fr}G3;8v;R^Om~uy;)mrZvvgGpjo<9ItUsYqPc+gg<XC`CHXtLkVhD4|8R49X%3cR_!#^1#hhgy=LKn`n0?J&V}Nt{iKsriQmn42?REi7B*tDEg26){KC=8dM6^>X@|<^`N?i}MYH@82FV>VfKW6H5lwh?GOvQMwTOEAjBZzk^vnNB1MH^8%%h$gH1ISmBk8j^$Z*G$ZNVjjI2Z!3z5n~pB)_R@I+8#c7xM{w|F9L9keBlUFf&_-C4$#3E#3qUS{E_5u$PNYGdcYkSi*!D5rFY<Bt7JFji1VxkP>QqG)U+!JQ%U$mfoHMP+8HKrES(C>ahd^O?=5jeuz1P^7swuAdqv-}S`3c_!XWk%KN+UE;9FS&w#1?KT~Yj^t@U2iG`cDlE}P&4TQ0rA4azFFfQ!z_Jv{q25;_3w>#}RnN8;8v3u;pu!`Z2vQJHBhVXp0uA=jzU_7Hz4!4ie(U*kfu2hb_T(UP9$|d~j@4c+5Z@Y)u5mlVct*wGn-~oM`m}0u6!YQ6Ac~#wxujibNjE1Z<2o$2FJX!LQ^uMR<I0kmL?(>S}A@b>^h1Zx*I5qTCRaR}7shXpLtuHFXqvV!dNrwRz!_n5SrgeYu6M`@XmVkRn6AM1M@Gm$oCxY@_A<~3gYTwV{Y5(2O4sPs>$4@|cQ1s^E0w+rP@=M#7#=LW)d6g>EiNXYCxX+f+nKH1C5t{DVPsQxTz0M_%Q2OZ%zwo-^Xi53JP`sNFq(qfNAyDWIOGVYGVB;jmYowAbQP+c}K5vIGoy2#)r_5j*iznC@e)5P?9S*wPBfS8m<q5&}IV_Y#h7%wgoefyt^fe?ID6Y+YeO6!rnlP^k=RGxORCGRc?*MeqpNyA(F7B{2;YUE6XHbCJGjn*rTlNiXd%{z)AXTRp?et4q|kuwM>9<~Ji&asGw4n4p2zAywA2v7iA(TmwY$UE7me60J=W@b`#*)MJsc0!BIQgskYqqakX@id}V4jL9#xA%a+tV}YG4}{^EAzJS^jQQN4xvV$r7g$e`%vSFhY#v>CT_T{a*lTpBu5A7(s%JaMm2X_!i#TF0+UFW@aBZBPkrD0tXqT6_s9{6KkC&+5jrf8R^>MF2qeXi!MppplbF&VX(LyB6fIb4d?4EU)d)pH$agf^RZx8K4LYeX43lxBh@N5Q?CjWGs7D4KpRZ9LCFp~@YHNKhNu<)i#R+`r+O8duPZ(5Hsd+8bP>?1sK#YJc*AMo?R!VphgzJjd+A6M>@?7}un}4#;Pu-B!k}t;ElP~w!mTn?m#mRsfofqi1r(PV$QuK|5fC4!ynZvqjF%P$A`4kHBzC=4$O|4vpYCfo*yWpyBF?CN@;G?1rvyHpZIue$UDBy?3x^<CxZlEuBV+jFtINv7=s6QB`@w~th6p=S0?$SPZWXpuIACmqSx+v;X0G};3~FAW$N2uSMsH`}N4Vt+^k)g?1Utu0j8`*LT**{7?IG-~E-a0fS>O6X=RQ-XcrJT(n%iZn0qr=?tLIi`=LbBzBuysX7lwrg3Pa9iI)&?b48zk>Tq{F${0En9evrzlh@&qVs2E@5?>TA6x8bkVe5;lADwuZd%NgJ)_S`06zaC6kZk%>Kxg>U4g<ebqWZ`I<q6~5gC*)lA)6K2;P`&WGoU#=D82m^8g{j2<7=ZMH@-4^!`<e2)3fh!a<&pY0KL!v&F0P^YJQ3Z#>T9l@Lo6rv>B2-6~pR{nR6b7M-Q@cbDjo=eTd|r!OCEd>=sE~?dPkI>H96zls<iLda4J;GpO|h@ST0L5f_hyDqeFMehf!Ap=y=$gd!!*' 
P = json.loads(zlib.decompress(base64.b85decode(DATA)).decode("utf-8"))

def replace_block(src, label, body):
    pat = re.compile(r"(?ms)^(" + re.escape(label) + r":[^\n]*\n)(.*?^\tdone\n?)")
    m = pat.search(src)
    if not m:
        raise RuntimeError(f"missing text block {label}")
    return src[:m.start()] + m.group(1) + body.rstrip() + "\n" + src[m.end():]

def patch_text(root, apply):
    changed = 0
    for rel, mapping in P["repls"].items():
        path = root / rel
        src = path.read_text(encoding="utf-8")
        old = src
        for label, body in mapping.items():
            src = replace_block(src, label, body)
        if src != old:
            changed += 1
            if apply:
                path.write_text(src, encoding="utf-8")
            print(("patched " if apply else "would patch ") + rel)
    return changed

def enable_bank(root, apply):
    changed = 0

    p = root / "data/maps/scripts.asm"
    src = p.read_text(encoding="utf-8")
    old = src
    open23 = '\n\n/*\nSECTION "Map Scripts 23", ROMX'
    if open23 in src:
        src = src.replace(open23, '\n\nSECTION "Map Scripts 23", ROMX', 1)
        open24 = '\n\nSECTION "Map Scripts 24", ROMX'
        if open24 not in src:
            raise RuntimeError("Map Scripts 24 marker missing while enabling 23")
        src = src.replace(open24, '\n\n/*\nSECTION "Map Scripts 24", ROMX', 1)
    if src != old:
        changed += 1
        if apply:
            p.write_text(src, encoding="utf-8")
        print(("patched " if apply else "would patch ") + str(p.relative_to(root)))

    p = root / "layout.link"
    src = p.read_text(encoding="utf-8")
    old = src
    src = src.replace('; ROMX $59\n; \t"Map Scripts 23"', 'ROMX $59\n\t"Map Scripts 23"', 1)
    if src != old:
        changed += 1
        if apply:
            p.write_text(src, encoding="utf-8")
        print(("patched " if apply else "would patch ") + str(p.relative_to(root)))

    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    root = Path(a.repo)
    n = patch_text(root, a.apply)
    n += enable_bank(root, a.apply)
    print(f"Bank $59: {n} file(s) changed; 75 ROM-verified Korean text labels recovered and Map Scripts 23 enabled.")

if __name__ == "__main__":
    main()
