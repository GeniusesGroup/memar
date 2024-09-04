/* For license and copyright information please see the LEGAL file in the code repository */

package br_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_BusinessRuleID interface {
	BusinessRuleID() RuleUUID
}

// use in quiddity domain too.
type RuleUUID ut16.UUID
