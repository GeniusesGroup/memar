/* For license and copyright information please see the LEGAL file in the code repository */

package brs_p

import (
	cl "memar/computer/language"
	"memar/protocol"

	aa_p "org/modules/app-audit/protocol"
	bm_p "org/modules/business-module/protocol"
	br_p "org/modules/business-rule/protocol"
	bs_p "org/modules/business-service/protocol"
	storage_p "org/modules/storage/protocol"
)

// Statement (computer science) is a line of code written as part of a computer program
// Rule statement or condition&action or policy or execution set or parameters or decision or ...
type DataModel interface {
	br_p.Field_BusinessRuleID
	RuleStepID() uint8 // order of precedence
	cl.Field_Logical_Connective

	// invoice-summary.DataModel.PayablePrice > 50,000,000
	bm_p.Field_ModuleID
	FieldID() protocol.DataTypeID
	Operator() cl.ComparisonOperator
	FieldValue() []byte

	// call NotifyUser(UserID, InvoiceID)
	// or call UserEarnCoin(UserID, 500)
	ActionID() bs_p.ServiceUUID
	ActionValue() []byte // TODO::: field+value or just value??

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
