/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountCategory indicate the domain record data fields.
type DiscountCategory interface {
	DiscountID() DiscountUUID       //
	CategoryID() CategoryUUID       //
	MinAmount() uint64              // Minimum number to buy to use discount
	MaxAmount() uint64              // Maximum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Type() DiscountCategory_Type    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountCategory_StorageServices interface {
	Save(dm DiscountCategory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountCategory, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_DiscountIDs_BY_CategoryID(categoryID CategoryUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type DiscountCategory_Type uint16

const (
	DiscountCategory_Type_Unset     DiscountCategory_Type = 0           //
	DiscountCategory_Type_Mandatory DiscountCategory_Type = (1 << iota) // != optional
	DiscountCategory_Type_Pair                                          //
)
