/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// TaskRelationUser indicate the domain record data fields.
type TaskRelationUser interface {
	TaskID() TaskUUID                    //
	UserID() up.UserUUID                 //
	RelationType() TaskRelationUser_Type //
	Time() protocol.Time                 // Save time
	RequestID() urp.UserRequestUUID      //
}

type TaskRelationUser_StorageServices interface {
	Save(f TaskRelationUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, taskID TaskUUID, vo protocol.VersionOffset) (f TaskRelationUser, nv protocol.NumberOfVersion, err protocol.Error)
}

type TaskRelationUser_Type uint8

const (
	TaskRelationUser_Type_Unset TaskRelationUser_Type = iota
	TaskRelationUser_Type_Participant
	TaskRelationUser_Type_Assigner
	TaskRelationUser_Type_Assigned
	TaskRelationUser_Type_Reviewer
	TaskRelationUser_Type_Approver
)
