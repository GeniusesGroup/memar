/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_RuleUUID interface {
	RuleUUID() UUID
}

type UUID record_p.UUID
