/* For license and copyright information please see the LEGAL file in the code repository */

package wrbl

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Reserved = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Occupied
	Status_Vacant
)
