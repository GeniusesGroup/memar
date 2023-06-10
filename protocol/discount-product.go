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
	Save(dm DiscountProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID, productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, productID ProductUUID, vo protocol.VersionOffset) (dm DiscountProduct, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_DiscountIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProductIDs_BY_DiscountID(discountID DiscountUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type DiscountProduct_Type uint16

const (
	DiscountProduct_Type_Unset     DiscountProduct_Type = 0           //
	DiscountProduct_Type_Mandatory DiscountProduct_Type = (1 << iota) // != optional
	DiscountProduct_Type_Pair                                         //
)
