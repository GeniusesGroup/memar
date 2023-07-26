/* For license and copyright information please see the LEGAL file in the code repository */

package smsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_NeedManagerApprove = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_ManagerApproved
)
