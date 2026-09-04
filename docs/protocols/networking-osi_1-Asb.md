# Asb - Physical Protocol

- This Frame structure will transport by physical layer so it is payload of desire frame and that frame have its header and structure like StartDelimiter, EndDelimiter, CheckSequence, ...

## Hardwares
Chapar functions can add by switching fabric unit (SFU) in any devices by any interfaces like PCIe, .... It can have 1 to 256 wired port or 2^16(65536) wireless port. 

### Core
The line processing unit (LPU) provides physical interfaces connecting the SFU(switching fabric unit) to external networks. The LPU processes and forwards service data. In addition, the LPU maintains and manages link protocols and frames congestions.

### Port Types
- RJ45 Port. RJ45 port (on 100/1000BASE Ethernet layer one) can be used in most cases.
- SFP Port
- SFP+ Port
- SFP28 Port
- QSFP+ Port
- QSFP28 Port
- Combo Port
- Stack Port

### Adaptor
Suggest to be addable port protocol like [SFP](https://en.wikipedia.org/wiki/Small_form-factor_pluggable_transceiver).

### Port Interfaces
offer diverse wired and wireless interfaces, for example, Ethernet(Layer1), [Power-line Communication](https://en.wikipedia.org/wiki/Power-line_communication), radio frequency(RF), RS485, RS232, ...

### Wireless Access Point
Each Chapar wireless ap device handles two hops of the frame instead of regular one hop in each switching hop. It means each wireless ap can serve 2^16(65536) devices.
Like other wireless technology, We must provide some dedicate channel:
- Broadcast control channel (BCCH) to manage broadcasting for all user equipment
- Paging control channel (PCCH) to manage paging messages --- why not page device by DTCH?????
- Common control channel (CCCH) and dedicated control channel (DCCH) for common messages for all user equipment in the same cell
- Dedicated traffic channel (DTCH) to send data to the specific user equipment in a cell

Use channel 49 (694-790 MHz) in [UHF](https://en.wikipedia.org/wiki/Ultra_high_frequency) frequency range to broadcast available 

Each Chapar wireless ap device handles two hops of the frame instead of regular one hop in each switching hop. It means each wireless ap can serve 2^16(65536) devices. Chapar can help layer 1 protocols to made connections betweeen AP and clients.