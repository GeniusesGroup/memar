/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// DiscountCategory indicate the domain record data fields.
type DiscountCategory interface {
	DiscountID() DiscountUUID       // discount domain
	CategoryID() [16]byte           // category domain
	MinAmount() uint64              // Minimum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type DiscountCategory_StorageServices interface {
	Save(dc DiscountCategory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID, categoryID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID, categoryID [16]byte, vo protocol.VersionOffset) (dc DiscountCategory, nv protocol.NumberOfVersion, err protocol.Error)

	ListDiscounts(categoryID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListCategories(discountID [16]byte, offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
