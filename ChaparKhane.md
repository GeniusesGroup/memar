# ChaparKhane - Router Server
ChaparKhane use to be gateway and route [GP protocol](./GP.md) packets inside XPs or to other XPs! ChaparKhane can also be as coordinator in networks without need GP packets come to ChaparKhane to route!!

## XP - Exchange Point (similar to IXP)
- Each XP can have many GP Router with multi path data-link connection! that has two type connection
    - Connection to same XP routers to route income or outcome frames.
    - Connection to one or more other XP Routers with direct or tunnel physical links by using other XP links! Tunnel connections are optional and just for decrease latency due to less frame or packet routing needed!
- Routers must broadcast any change to data-link address to the shared database!
- Each XP obtain just one unique 32-bit unsigned integer for routing in its database and tell all adjacent physical connected XPs about existence! So XP can just register a 32-bit address just if it has a direct link to some other XPs.
- We must rule to make XPs network grows slowly.

## GP Routers (similar to ISP)
- Each 32bit range GP (as max apps can lease GPs) has a public key that generates in negotiated by XP and App router(owner of GP).
- Each GP packet encrypts in OS and App layer by paired EncryptionKey before sending. This way no GP Address can steal by others!

## ChaparKhane word meaning
["Chapar Khaneh"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپارخانه‎, IPA: [tʃɒːˈpɒːɾ xɒːˈne], courier-house) is a Persian term for the postal service used during the Achaemenid era. The system was created by Cyrus the Great, the founder of the Persian Empire, and later developed by Darius the Great, as the royal method of communication throughout the empire. Each "Chapar Khaneh" was a station mainly located along the Royal Road, a 2500 km ancient highway, which stretched from the Sardis to Susa, connecting most of the major cities of the empire.