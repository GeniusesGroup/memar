/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectLabel indicate the domain record data fields.
type ProjectLabel interface {
	ProjectID() ProjectUUID         //
	LabelID() LabelUUID             //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type ProjectLabel_StorageServices interface {
	Save(p ProjectLabel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID [16]byte, vo protocol.VersionOffset) (p ProjectLabel, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByType(typ Product_Type, offset, limit uint64) (projectIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
