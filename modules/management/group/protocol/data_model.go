/* For license and copyright information please see the LEGAL file in the code repository */

package group_p

import (
	event_p "memar/process/event/protocol"
)

type DataModel interface {
	Field_GroupID

	event_p.Event
}
