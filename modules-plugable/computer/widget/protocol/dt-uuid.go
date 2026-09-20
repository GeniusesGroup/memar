/* For license and copyright information please see the LEGAL file in the code repository */

package widget_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_WidgetID interface {
	WidgetID() UUID
}

type UUID thing_p.UUID
