/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// DiscountProduct or product sale indicate the domain record data fields.
type DiscountProduct interface {
	DiscountID() DiscountUUID       //
	ProductID() ProductUUID         //
	MinAmount() uint64              // Minimum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type DiscountProduct_StorageServices interface {
	Save(dp DiscountProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID, productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID, productID [16]byte, vo protocol.VersionOffset) (dp DiscountProduct, nv protocol.NumberOfVersion, err protocol.Error)

	ListDiscounts(productID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListProducts(discountID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
