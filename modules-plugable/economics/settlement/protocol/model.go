/* For license and copyright information please see the LEGAL file in the code repository */

package settlement_p

import (
	event_p "memar/process/event/protocol"

	rule_p "org/modules/computer/rule/protocol"
	thing_p "org/modules/identity/thing/protocol"
)

type Model interface {
	thing_p.Model
	rule_p.Model

	event_p.Target[DataModel]
}
