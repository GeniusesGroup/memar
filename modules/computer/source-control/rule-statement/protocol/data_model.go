/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

import (
	datatype_p "memar/computer/datatype/protocol"
	"memar/math/logic"
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	rule_p "org/modules/computer/rule/protocol"
)

// TODO::: Below data model doesn't work by many reason!
// Remove it in favor of portable binaries like WASM???

// Statement (computer science) is a line of code written as part of a computer program
// Rule statement or condition&action or policy or execution set or parameters or decision or ...
type DataModel[CS Condition, AV ActionValue] interface {
	rule_p.Field_RuleUUID
	// Field_RuleStepID

	Conditions() []CS
	ActionValues() []AV

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

type Condition interface {
	// If not `UNSET`, check with next condition
	logic.Field_Logical_Connective

	// e.g.
	// - Service Called with No condition!
	// - invoice-summary.DataModel.PayablePrice > 50,000,000
	FieldID() datatype_p.ID
	Operator() logic.ComparisonOperator
	FieldValue() []byte
}

// call NotifyUser(UserID, InvoiceID)
// or call UserEarnCoin(UserID, 500)
type ActionValue interface {
	// If not `UNSET`, check with next condition
	logic.Field_Logical_Connective

	// UserID
	FieldID() datatype_p.ID

	// TODO::: how to point to other FieldValue e.g. UserID
	// TODO::: how provide this logic? `invoice.TotalPayment/1000`
	FieldValue() []byte
}
