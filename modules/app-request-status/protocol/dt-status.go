/* For license and copyright information please see the LEGAL file in the code repository */

package arsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Draft     = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Approving // AWAITING APPROVAL
	Status_Approved
	Status_Rejected
	Status_Processing // In progress, Pending
	Status_Processed  // Completed
	Status_Failed
	Status_Canceled
)

// COMPENSATED
