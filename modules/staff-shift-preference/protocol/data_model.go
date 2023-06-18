/* For license and copyright information please see the LEGAL file in the code repository */

package sspp

import (
	"libgo/protocol"
	"libgo/time/utc"

	osp "org/modules/org-shift/protocol"
	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID //
	Day() utc.DayElapsed   //
	ShiftID() osp.ShiftUUID
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
