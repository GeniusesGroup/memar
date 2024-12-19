/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

type Field_Type interface {
	Type() Type
}

type Type uint64

const Type_Unset Type = 0
const (
	// It means rule will execute only by call related service.
	// e.g. apply a voucher on an invoice just by enter voucher code by user in related input element.
	Type_Manual Type = (1 << iota)

	// It will part of process and can change the flow of the desire service (process)
	// e.g. by return an error.
	// ((Synchronous == false) == ASynchronous) It will call beside or after process and can't change the flow of the services.
	Type_Synchronous

	// It means rule not valid after a certain of times.
	Type_TimeLimit
)
