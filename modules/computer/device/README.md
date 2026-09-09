# Device
It is common modules for things or specific channel. Organizations can develop more specific modules for their custom hardwares.

## Smart Device

A [smart device](https://en.wikipedia.org/wiki/Smart_device) is an electronic device, generally connected to other devices or networks via different wireless protocols (such as Bluetooth, Zigbee, near-field communication, Wi-Fi, NearLink, Li-Fi, or 5G) that can operate to some extent interactively and autonomously. Several notable types of smart devices are smartphones, smart speakers, smart cars, smart cards, smart thermostats, smart doorbells, smart locks, smart refrigerators, phablets and tablets, smartwatches, smart bands, smart keychains, smart glasses, smart TV, and many others. The term can also refer to a device that exhibits some properties of ubiquitous computing, including—although not necessarily—machine learning.

Smart devices can be designed to support a variety of form factors, a range of properties pertaining to ubiquitous computing and to be used in three main system environments: physical world, human-centered environments, and distributed computing environments. Smart homes indicate the presence of sensors and some detection devices, appliances, and a database to control them.

## Internet of things

The [Internet of things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) describes physical objects that are embedded with sensors, processing ability, software, and other technologies that connect and exchange data with other devices and systems over the Internet or other communication networks. The IoT encompasses electronics, communication, and computer science engineering. "Internet of things" has been considered a misnomer because devices do not need to be connected to the public Internet; they only need to be connected to a network and be individually addressable.

The field has evolved due to the convergence of multiple technologies, including ubiquitous computing, commodity sensors, increasingly powerful embedded systems, and machine learning. Traditional fields of embedded systems, wireless sensor networks, and control systems independently and collectively enable the Internet of Things.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Channel status - edges/thing-channel-status.go
- **Idea**: channel states Off/Offline; both marked with the same TODO: the status may instead indicate in a thing-signal (or IO) subdomain as the state of a channel, e.g. an off state needing to change the LED state on the thing cover.
- **Review questions**: which domain owns channel state? Does the status drive physical indicators?

### Thing-organization relation - edges/thing-relation-org.go
- **Idea**: Producer/Consumer labels between things (or their channels) and organizations; triple sketch [Thing, Organization, Label] / [Channel, Organization, Label].
- **Review questions**: is Producer/Consumer an edge to Organization or a label? Where does it intersect the economics product chain?