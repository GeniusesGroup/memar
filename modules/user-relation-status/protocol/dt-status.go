/* For license and copyright information please see the LEGAL file in the code repository */

package ursp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Blocked = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Muted
)
