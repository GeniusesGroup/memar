/* For license and copyright information please see the LEGAL file in the code repository */

package rrop

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrganizationID() org.OrgUUID    //
	RoleID() rp.RoleUUID            //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
