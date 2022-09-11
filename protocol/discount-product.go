/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountProduct or product sale indicate the domain record data fields.
type DiscountProduct interface {
	DiscountID() [16]byte           // discount domain
	ProductID() [16]byte            // product domain
	MinAmount() uint64              // Minimum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type DiscountProduct_StorageServices interface {
	Save(dp DiscountProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dp DiscountProduct, nv protocol.NumberOfVersion, err protocol.Error)

	FindByProduct(productID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
