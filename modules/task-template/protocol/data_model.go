/* For license and copyright information please see the LEGAL file in the code repository */

package ttp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskTemplateID() TaskTemplateUUID //
	UserID() up.UserUUID              //
	// TODO::: group of comment?? questionnaire??
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
