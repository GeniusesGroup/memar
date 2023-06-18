/* For license and copyright information please see the LEGAL file in the code repository */

package ptp

import (
	"libgo/protocol"

	pp "org/modules/project/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	ExpectedTime() protocol.Time    //
	Deadline() protocol.Time        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
