/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountProduct or product sale indicate the domain record data fields.
type DiscountProduct interface {
	DiscountID() DiscountUUID       //
	ProductID() ProductUUID         //
	MinAmount() uint64              // Minimum number to buy to use discount
	MaxAmount() uint64              // Maximum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Type() DiscountProduct_Type     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountProduct_StorageServices interface {
	Save(dp DiscountProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID, productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID, productID [16]byte, vo protocol.VersionOffset) (dp DiscountProduct, nv protocol.NumberOfVersion, err protocol.Error)

	ListDiscounts(productID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListProducts(discountID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type DiscountProduct_Type uint16

const (
	DiscountProduct_Type_Unset     DiscountProduct_Type = 0           //
	DiscountProduct_Type_Mandatory DiscountProduct_Type = (1 << iota) // != optional
	DiscountProduct_Type_Pair                                         //
)
