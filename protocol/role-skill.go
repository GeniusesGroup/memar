/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleSkill indicate the domain record data fields.
type RoleSkill interface {
	RoleID() RoleUUID
	SkillID() SkillUUID
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleSkill_StorageServices interface {
	Save(dm RoleSkill) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (dm RoleSkill, nv protocol.NumberOfVersion, err protocol.Error)
}
