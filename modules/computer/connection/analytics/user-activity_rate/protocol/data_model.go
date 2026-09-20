/* For license and copyright information please see the LEGAL file in the code repository */

package uaarp

import (
	"memar/time/utc"

	user_p "org/modules/identity/user/protocol"
)

type DataModel interface {
	user_p.Field_UserUUID
	utc.Field_HourElapsed
	Rate() Rate
}
