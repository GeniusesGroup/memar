/* For license and copyright information please see the LEGAL file in the code repository */

package authorized_p

import (
	rule_p "org/modules/computer/rule/protocol"
)

type Field_AuthorizedBy interface {
	AuthorizedBy() rule_p.UUID
}
