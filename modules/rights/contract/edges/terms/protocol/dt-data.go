/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	module_p "org/modules/computer/module/protocol"
	thing_p "org/modules/identity/thing/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

type Field_Data interface {
	Data() []Data
}

type Data struct {
	label label_p.UUID
	// This ID can point to `knowledge/text` module to store some human string.
	id       thing_p.UUID
	moduleID module_p.UUID
}
