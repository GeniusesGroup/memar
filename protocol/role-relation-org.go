/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// RoleOrganizationRelation indicate the domain record data fields.
type RoleOrganizationRelation interface {
	OrganizationID() OrgUUID        //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type RoleOrganizationRelation_StorageServices interface {
	Save(dm RoleOrganizationRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(organizationID OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(organizationID OrgUUID, vo protocol.VersionOffset) (dm RoleOrganizationRelation, nv protocol.NumberOfVersion, err protocol.Error)
}
