/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type TaskTemplateUUID = protocol.UUID

// Task indicate the domain record data fields.
type TaskTemplate interface {
	TaskTemplateID() TaskTemplateUUID //
	UserID() UserUUID                 //
	// TODO::: group of comment?? questionnaire??
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}
