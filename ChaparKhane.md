# ChaparKhane - Router Server
ChaparKhane use to be gateway and route [GP protocol](./GP.md) packets inside a society network or to other societies! ChaparKhane can also be as coordinator in networks without need GP packets come to ChaparKhane to route!!

## Society network - Similar to IXP (Internet Exchange Point)
- Each society can have many ChaparKhane(GP Router) with multi path data-link connection! that has two type connection
    - Connection to same society ChaparKhane(GP Routers) to route income or outcome packets.
    - Connection to one or more other society ChaparKhane(GP Routers) with direct or tunnel physical links by using other society links! Tunnel connections are optional and just for decrease latency due to less frame or packet routing needed!
- ChaparKhane(GP Routers) must broadcast any change to data-link address to others!

## GP Routers (similar to ISP)
- Each 32bit range GP (as max apps can lease GPs) has a public key that generates in negotiated by society and App router(owner of GP).
- Each GP packet encrypts in OS and App layer by paired EncryptionKey before sending. This way no GP Address can steal by others!

## Implemented Library
We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/ChaparKhane) and more in progress. Easily make an ChaparKhane router app with these libraries.

## ChaparKhane word meaning
["Chapar Khaneh"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپارخانه‎, IPA: [tʃɒːˈpɒːɾ xɒːˈne], courier-house) is a Persian term for the postal service used during the Achaemenid era. The system was created by Cyrus the Great, the founder of the Persian Empire, and later developed by Darius the Great, as the royal method of communication throughout the empire. Each "Chapar Khaneh" was a station mainly located along the Royal Road, a 2500 km ancient highway, which stretched from the Sardis to Susa, connecting most of the major cities of the empire.
