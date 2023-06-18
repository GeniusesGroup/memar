/* For license and copyright information please see the LEGAL file in the code repository */

package srp

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID          //
	ReferralID() up.UserUUID        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
