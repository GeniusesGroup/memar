/* For license and copyright information please see the LEGAL file in the code repository */

package fs_p

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Terminated = Status(qsp.Quiddity_Status_FreeFlag << iota) // Wait to approve
)
