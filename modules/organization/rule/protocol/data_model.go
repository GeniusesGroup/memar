/* For license and copyright information please see the LEGAL file in the code repository */

package br_p

import (
	aa_p "org/modules/app-audit/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	Field_BusinessRuleID
	Field_LogicType

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
