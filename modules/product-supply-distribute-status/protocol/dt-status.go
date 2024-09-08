/* For license and copyright information please see the LEGAL file in the code repository */

package icsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

// overall status
type Status qsp.Quiddity_Status

// DC abbreviation for distribution-center or Warehouse
const (
	Status_OutcomeDCRequested = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_IncomeDCRequested
	Status_OutcomeDCApproved
	Status_IncomeDCApproved
	Status_Void
)
