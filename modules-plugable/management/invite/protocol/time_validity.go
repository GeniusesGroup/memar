/* For license and copyright information please see the LEGAL file in the code repository */

package ig_p

import (
	time_p "memar/time/protocol"
)

type TimeValidity interface {
	Start() time_p.Time
	End() time_p.Time
}
