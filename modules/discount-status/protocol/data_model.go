/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Expired = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_End
)
