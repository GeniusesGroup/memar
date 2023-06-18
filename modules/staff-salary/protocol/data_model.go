/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel is fixed negotiated salary that don't follow org||department||role salary rules.
type DataModel interface {
	StaffID() sp.StaffUUID              //
	WeeklySalary() protocol.MoneyAmount //
	SaveTime() protocol.Time            //
	RequestID() urp.UserRequestUUID     //
}
