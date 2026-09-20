/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	fmp "org/modules/economics/money/protocol"
	product_p "org/modules/economics/product/protocol"
)

// DataModel or product sale indicate the domain record data fields.
type Product interface {
	product_p.Field_ProductID
	MinAmount() uint64    // Minimum number to buy to use discount
	MaxAmount() uint64    // Maximum number to buy to use discount
	MinPrice() fmp.Amount // Minimum price to buy to use discount
	MinStock() uint64     // 0 for unlimited until related product exist to sell
	Type() Type
}

type Type uint16

const (
	Type_Unset     Type = 0           //
	Type_Mandatory Type = (1 << iota) // != optional
	Type_Pair                         //
)
