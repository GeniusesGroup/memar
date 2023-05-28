/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectTable indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
type ProjectRelationTable interface {
	ProjectID() ProjectUUID         //
	TableID() TableUUID             //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type ProjectRelationTable_StorageServices interface {
	Save(f ProjectRelationTable) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, vo protocol.VersionOffset) (f ProjectRelationTable, nv protocol.NumberOfVersion, err protocol.Error)
}
