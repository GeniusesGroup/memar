/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectRelationProject indicate the domain record data fields.
type ProjectRelationProject interface {
	ProjectID() ProjectUUID            //
	OtherID() ProjectUUID              //
	Priority() uint64                  //
	Type() ProjectRelationProject_Type //
	Time() protocol.Time               // Save time
	RequestID() urp.UserRequestUUID    //
}

type ProjectRelationProject_Type uint8

// Blocking

type ProjectRelationProject_StorageServices interface {
	Save(f ProjectRelationProject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(otherID ProjectUUID, projectID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(otherID ProjectUUID, projectID ProjectUUID, vo protocol.VersionOffset) (f ProjectRelationProject, nv protocol.NumberOfVersion, err protocol.Error)
}
