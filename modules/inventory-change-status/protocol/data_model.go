/* For license and copyright information please see the LEGAL file in the code repository */

package picsp

import (
	"libgo/protocol"

	icp "org/modules/inventory-change/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InventoryChangeID() icp.InventoryChangeUUID //
	Status() Status                              // overall
	SaveTime() protocol.Time                     //
	RequestID() urp.UserRequestUUID              //
}

type Status qsp.Quiddity_Status

// DC abbreviation for distribution-center or Warehouse
const (
	Status_OutcomeDCRequested = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_IncomeDCRequested
	Status_OutcomeDCApproved
	Status_IncomeDCApproved
	Status_Void
)
