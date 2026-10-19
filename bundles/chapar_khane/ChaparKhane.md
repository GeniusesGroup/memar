# ChaparKhane - Router Server
ChaparKhane use to be gateway and route GP protocol (./networking-osi_3-Giti-Network.md) packets inside a society network or to other societies! ChaparKhane can also be as coordinator in networks without need GP packets or Chapar frames come to ChaparKhane to route or switch!!

## Society network - Similar to IXP (Internet Exchange Point)
- Each society can have many ChaparKhane(GP Router) with multi path data-link connection! that has two type connection
    - Connection to same society ChaparKhane(GP Routers) to route income or outcome packets.
    - Connection to one or more other society ChaparKhane(GP Routers) with direct or tunnel physical links by using other society links! Tunnel connections are optional and just for decrease latency due to less frame or packet routing needed!
- ChaparKhane(GP Routers) must broadcast any change to data-link address to others!

## GP Routers (similar to ISP)
- Each 32bit range GP (as max apps can lease GPs) has a public key that generates in negotiated by society and App router(owner of GP).
- Each GP packet encrypts in OS and App layer by paired EncryptionKey before sending. This way no GP Address can steal by others!

## Implemented Library
We implement it on some language like [C], [Go](https://github.com/GeniusesGroup/libgo/blob/master/ChaparKhane) and more in progress. Easily make an ChaparKhane router app with these libraries.

## ChaparKhane word meaning
["Chapar Khaneh"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپارخانه‎, IPA: [tʃɒːˈpɒːɾ xɒːˈne], courier-house) is a Persian term for the postal service used during the Achaemenid era. The system was created by Cyrus the Great, the founder of the Persian Empire, and later developed by Darius the Great, as the royal method of communication throughout the empire. Each "Chapar Khaneh" was a station mainly located along the Royal Road, a 2500 km ancient highway, which stretched from the Sardis to Susa, connecting most of the major cities of the empire.

## Idea backlog from service code comments

Nothing below is ratified. Prefer existing homes over inventing new modules.

### Router discovery
- **Idea**: Unlike router solicitation, discovery use to find the specific router by its ID!
- **Review questions**: bundle test - this bundle owns no kernel schema; is ID-based discovery protocol behavior of the composed GP routing capability (service processing), and who maintains the router-ID records?

### GP from master routers
- **Idea**: Can get GP by some master routers!
- **Review questions**: bundle test - GP issuance semantics live in the composed GP/router capability, not the bundle; who authorizes a master router to hand out GPs, and does that authorization become a rule (core never knows rule) rather than bundle logic?
