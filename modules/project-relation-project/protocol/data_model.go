/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"libgo/protocol"

	pp "org/modules/project/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	OtherID() pp.ProjectUUID        //
	Priority() uint64               //
	Type() Type                     //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

type Status qsp.Quiddity_Status
