/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DepartmentOrgRelation indicate the domain record data fields.
type DepartmentOrgRelation interface {
	DepartmentID() DepartmentUUID   //
	OrganizationID() OrgUUID        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
