/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// OrderStatus indicate the order-status domain record data fields.
type OrderStatus interface {
	OrderID() [16]byte          // order domain
	Status() Order_Status       //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type OrderStatus_StorageServices interface {
	Save(os OrderStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (os OrderStatus, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Order_Status, offset, limit uint64) (orderIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	// protocol.EventTarget
}

type Order_Status Quiddity_Status

const (
	Order_Status_Pending = Order_Status(Quiddity_Status_FreeFlag << iota) // Wait to approve
	Order_Status_NeedApprovement
	Order_Status_Approved
	Order_Status_PartiallyDeal
	Order_Status_FullyDeal
	Order_Status_Expired
	Order_Status_Cancelled // Voided
)
