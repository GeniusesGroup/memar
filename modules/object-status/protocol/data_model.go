/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ObjectID() op.ObjectUUID        //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// Object_Status_ Status = (Quiddity_Status_FreeFlag << iota)
)
