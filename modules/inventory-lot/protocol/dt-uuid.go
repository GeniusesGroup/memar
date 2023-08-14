/* For license and copyright information please see the LEGAL file in the code repository */

package ilp

import (
	"memar/protocol"
)

// A lot number is an identification number assigned to a particular quantity or lot of material from a single manufacturer.
// Lots correspond to a certain number of products you received and store altogether in one single pack.
// https://en.wikipedia.org/wiki/Lot_number
type LotUUID protocol.UUID
