/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the order-status domain record data fields.
type DataModel interface {
	OrderID() op.OrderUUID          //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Pending = Status(qsp.Quiddity_Status_FreeFlag << iota) // Wait to approve
	Status_NeedApprovement
	Status_Approved
	Status_PartiallyDeal
	Status_FullyDeal
	Status_Expired
	Status_Cancelled // Voided
)
