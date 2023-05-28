/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectTiming indicate the domain record data fields.
type ProjectTiming interface {
	ProjectID() ProjectUUID         //
	ExpectedTime() protocol.Time    //
	Deadline() protocol.Time        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}


type ProjectTiming_StorageServices interface {
	Save(f ProjectTiming) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, vo protocol.VersionOffset) (f ProjectTiming, nv protocol.NumberOfVersion, err protocol.Error)
}
