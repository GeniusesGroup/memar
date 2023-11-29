/* For license and copyright information please see the LEGAL file in the code repository */

package uaacuhp

import( 
	"memar/protocol"
 "memar/time/utc"
up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	Hour() utc.HourElapsed
	OnlineCount() OnlineCount
}
