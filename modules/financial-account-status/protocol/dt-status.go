/* For license and copyright information please see the LEGAL file in the code repository */

package fasp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Closed = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
