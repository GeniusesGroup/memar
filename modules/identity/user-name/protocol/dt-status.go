/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	qsp "org/modules/quiddity-status/protocol"
)

// Status indicate UserName record status
type Status qsp.Quiddity_Status

// UserName status
const (
	Status_Reserved = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
