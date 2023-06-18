/* For license and copyright information please see the LEGAL file in the code repository */

package qmsp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qsp "org/modules/quiddity-status/protocol"
	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	QuiddityID() qp.QuiddityUUID    //
	ObjectID() op.ObjectUUID        // media file
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
// Status_ Status = (Quiddity_Status_FreeFlag << iota)
)
