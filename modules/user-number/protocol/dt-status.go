/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	qsp "org/modules/quiddity-status/protocol"
)

// Status indicate UserNumber record status
type Status qsp.Quiddity_Status

const (
	Status_Approved = Status(qsp.Quiddity_Status_FreeFlag << iota)
	// Status_Hidden		in this case user can't login by number
)
