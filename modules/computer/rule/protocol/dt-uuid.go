/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_RuleID interface {
	RuleID() UUID
}

type UUID quiddity_p.UUID
