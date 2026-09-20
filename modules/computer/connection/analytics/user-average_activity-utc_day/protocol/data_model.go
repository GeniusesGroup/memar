/* For license and copyright information please see the LEGAL file in the code repository */

package uataahp

import (
	"memar/time/duration"
	"memar/time/utc"

	user_p "org/modules/identity/user/protocol"
)

type DataModel interface {
	user_p.Field_UserUUID
	utc.Field_DayElapsed
	TimeSpend() duration.Second
	Average() Average
}
