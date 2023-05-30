/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleOrganizationRelation indicate the domain record data fields.
type RoleOrganizationRelation interface {
	RoleID() RoleUUID               //
	OrganizationID() OrgUUID        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleOrganizationRelation_StorageServices interface {
	Save(sf RoleOrganizationRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID RoleUUID, vo protocol.VersionOffset) (sf RoleOrganizationRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOrg(organizationID OrgUUID, offset, limit uint64) (roleID []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
