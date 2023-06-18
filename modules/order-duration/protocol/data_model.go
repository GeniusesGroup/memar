/* For license and copyright information please see the LEGAL file in the code repository */

package odp

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	OrderID() op.OrderUUID          //
	Epoch() OrderDuration_Epoch     //
	Duration() protocol.Duration    // from Epoch()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type OrderDuration_Epoch uint8

const (
	OrderDuration_Epoch_Unset OrderDuration_Epoch = iota
	OrderDuration_Epoch_IssueDate
	OrderDuration_Epoch_LastSuggest
	OrderDuration_Epoch_LastDeal
)
