/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProjectProductRelation indicate the domain record data fields.
type ProjectGroupRelation interface {
	ProjectID() ProjectUUID                          //
	GroupID() GroupUUID                              //
	ProjectGroupRelation() ProjectGroupRelation_Type //
	Time() protocol.Time                             // Save time
	RequestID() urp.UserRequestUUID                  //
}

type ProjectGroupRelation_StorageServices interface {
	Save(dm ProjectGroupRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(projectID ProjectUUID, GroupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(projectID ProjectUUID, GroupID GroupUUID, vo protocol.VersionOffset) (dm ProjectGroupRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_GroupIDs_BY_ProjectIDs(projectID ProjectUUID, offset, limit uint64) (GroupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProjectIDs_BY_GroupID(GroupID GroupUUID, offset, limit uint64) (projectIDs []ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProjectGroupRelation_Type uint8

const (
	ProjectGroupRelation_Type_Unset ProjectGroupRelation_Type = iota
	ProjectGroupRelation_Type_Authorization
)


// 	LIST_ProjectIDs_By_GroupID_AND_Type(GroupID GroupUUID, t ProjectGroupRelation_Type, offset, limit uint64) (projectIDs []ProjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
