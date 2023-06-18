/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	"libgo/protocol"

	pp "org/modules/project/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	Status() Status                 //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
