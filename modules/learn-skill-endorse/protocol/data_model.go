/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	sp "org/modules/learn-skill/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID            //
	SkillID() sp.SkillUUID          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
