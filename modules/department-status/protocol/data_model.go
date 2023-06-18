/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"libgo/protocol"

	dp "org/modules/department/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DepartmentStatus interface {
	DepartmentID() dp.DepartmentUUID //
	Status() Status                  //
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}

type Status qsp.Quiddity_Status

const (
// Status_ Status = (Quiddity_Status_FreeFlag << iota)
)
