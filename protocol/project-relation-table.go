/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectTable indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
type ProjectRelationTable interface {
	ProjectID() ProjectUUID //
	TableID() TableUUID     //
	Status() ProjectRelationTable_Status
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type ProjectRelationTable_StorageServices interface {
	Save(dm ProjectRelationTable) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, tableID TableUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, tableID TableUUID, vo protocol.VersionOffset) (dm ProjectRelationTable, nv protocol.NumberOfVersion, err protocol.Error)
}

// 	LIST_TableIDs_BY_ProjectID(projectID ProjectUUID, offset, limit uint64) (tableIDs []TableUUID, nv protocol.NumberOfVersion, err protocol.Error)

type ProjectRelationTable_Status Quiddity_Status
