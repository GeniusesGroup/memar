/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserSkillEndorse indicate the domain record data fields.
type UserSkillEndorse interface {
	UserID() UserUUID               //
	SkillID() SkillUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
