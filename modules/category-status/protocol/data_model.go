/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	cp "org/modules/category/protocol"
	qsp "org/modules/quiddity-status/protocol"
)

type DataModel interface {
	CategoryID() cp.CategoryUUID    //
	Status() Status        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}



type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
