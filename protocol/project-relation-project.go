/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectRelationProject indicate the domain record data fields.
type ProjectRelationProject interface {
	ProjectID() ProjectUUID                //
	OtherID() ProjectUUID                  //
	Priority() uint64                      //
	Type() ProjectRelationProject_Type     //
	Status() ProjectRelationProject_Status //
	Time() protocol.Time                   // Save time
	RequestID() urp.UserRequestUUID        //
}

type ProjectRelationProject_Type uint8

// Blocking

type ProjectRelationProject_StorageServices interface {
	Save(dm ProjectRelationProject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, otherID ProjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, otherID ProjectUUID, vo protocol.VersionOffset) (dm ProjectRelationProject, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_OtherIDs_BY_ProjectID(projectID ProjectUUID, offset, limit uint64) (OtherIDs []ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// 	LIST_ProjectIDs_BY_OtherID_AND_Type(otherID ProjectUUID, t ProjectRelationProject_Type, offset, limit uint64) (projectIDs []ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)


type ProjectRelationProject_Status Quiddity_Status