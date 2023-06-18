/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID      //
	Status() Status         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
