/* For license and copyright information please see the LEGAL file in the code repository */

package uataahp

import (
	"memar/protocol"
	"memar/time/utc"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	Day() utc.DayElapsed
	TimeSpend() protocol.Duration
	Average() Average
}
