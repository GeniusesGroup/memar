/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type TaskTemplateUUID = protocol.UUID

// Task indicate the domain record data fields.
type TaskTemplate interface {
	TaskTemplateID() TaskTemplateUUID //
	UserID() up.UserUUID              //
	// TODO::: group of comment?? questionnaire??
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type TaskTemplate_StorageServices interface {
	Save(f TaskTemplate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(taskID TaskUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(taskID TaskUUID, vo protocol.VersionOffset) (f TaskTemplate, nv protocol.NumberOfVersion, err protocol.Error)
}
