/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	fmp "org/modules/fields/money/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel can be register just by producer organization whom own the related quiddity
type DataModel interface {
	Price() fmp.Amount // Basic Price, not payable price, in the currency
}
