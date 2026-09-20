/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	"memar/math/per"

	fmp "org/modules/economics/money/protocol"
)

type Value interface {
	Quantity() per.Myriad // max discount percentage for each invoices, products, ... price
	Price() fmp.Amount    // max discount price can use for each invoices, product, ... price
}
