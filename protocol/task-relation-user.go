/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TaskRelationUser indicate the domain record data fields.
type TaskRelationUser interface {
	TaskID() TaskUUID                    // quiddity domain. use to get and show locale title.
	UserID() protocol.UserID             // user-status domain
	RelationType() TaskRelationUser_Type //
	Time() protocol.Time                 // Save time
	RequestID() urp.UserRequestUUID      // user-request domain
}

type TaskRelationUser_Type uint8

const (
	TaskRelationUser_Type_Unset TaskRelationUser_Type = iota
	TaskRelationUser_Type_Participant
	TaskRelationUser_Type_Assigner
	TaskRelationUser_Type_Assigned
	TaskRelationUser_Type_Owner
	TaskRelationUser_Type_Reviewer
)
