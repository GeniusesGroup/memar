/* For license and copyright information please see the LEGAL file in the code repository */

package rrdp

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	qsp "org/modules/quiddity-status/protocol"
	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID //
	Status() Status
	DepartmentID() dp.DepartmentUUID //
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}

type Status qsp.Quiddity_Status
