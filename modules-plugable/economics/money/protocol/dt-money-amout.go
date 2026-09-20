/* For license and copyright information please see the LEGAL file in the code repository */

package money_p

type Field_Amount interface {
	// Amount is transaction level amount
	MoneyAmount() Amount
}

// Amount a quantity of money
// Some number base on currency is Decimal part e.g. 8099 >> 80.99$
type Amount int64
