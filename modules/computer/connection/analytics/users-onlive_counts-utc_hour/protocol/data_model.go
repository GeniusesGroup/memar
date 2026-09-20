/* For license and copyright information please see the LEGAL file in the code repository */

package uaachp

import (
	"memar/time/earth"
)

type DataModel interface {
	Hour() earth.Hour
	OnlineCounts() OnlineCount
}
