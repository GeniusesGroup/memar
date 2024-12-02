/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Terminated = Status(qsp.Quiddity_Status_FreeFlag << iota) // Wait to approve
)
