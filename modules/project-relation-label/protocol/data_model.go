/* For license and copyright information please see the LEGAL file in the code repository */

package prlp

import (
	"libgo/protocol"

	lp "org/modules/label/protocol"
	pp "org/modules/project/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	LabelID() lp.LabelUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
