/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type OrderDuration interface {
	OrderID() [16]byte           // order domain
	Epoch() OrderDuration_Epoch  //
	Duration() protocol.Duration // from Epoch()
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type OrderDuration_StorageServices interface {
	Save(od OrderDuration) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID [16]byte, vo protocol.VersionOffset) (od OrderDuration, nv protocol.NumberOfVersion, err protocol.Error)
}

type OrderDuration_Epoch uint8

const (
	OrderDuration_Epoch_Unset OrderDuration_Epoch = iota
	OrderDuration_Epoch_IssueDate
	OrderDuration_Epoch_LastSuggest
	OrderDuration_Epoch_LastDeal
)
