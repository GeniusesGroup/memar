/* For license and copyright information please see the LEGAL file in the code repository */

package nla_p

import (
	time_p "memar/time/protocol"
)

type DataModel interface {
	LastAcknowledge() time_p.Time // e.g utc.Time
}
