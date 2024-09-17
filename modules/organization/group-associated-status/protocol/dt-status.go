/* For license and copyright information please see the LEGAL file in the code repository */

package gasp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Joined = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Blocked
	Status_Muted

	Status_WaitToAcceptByAdmins
	Status_WaitToAcceptByUser
)
