/* For license and copyright information please see the LEGAL file in the code repository */

package cpksp

import (
	qsp "org/modules/quiddity-status/protocol"
)

// Status use to indicate UserPublicKey record status
type Status qsp.Quiddity_Status

// UserPublicKey status
const (
	Status_Active = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Blocked
	Status_Revoked
)
