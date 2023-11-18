/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	np "org/modules/node/protocol"
)

type DataModel interface {
	NodeID() np.UUID
	AddressType() Type
	Address() Address
	AddressBinary() []byte
}
